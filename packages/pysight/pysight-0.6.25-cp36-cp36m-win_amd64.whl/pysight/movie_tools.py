"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = Hagai Hargil
"""
import attr
from attr.validators import instance_of
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Iterator, Tuple, Iterable, Dict
from numba import jit, float64, uint64, int64
from collections import OrderedDict, namedtuple, deque
import warnings
import h5py_cache
from tqdm import tqdm


def trunc_end_of_file(name) -> str:
    """
    Take only the start of the filename to avoid error with Python and Windows
    :param name: File name to truncate.
    :return:
    """
    return name[:240]


@attr.s
class Movie(object):
    """
    A holder for Volume objects to be displayed consecutively.
    """
    data            = attr.ib()
    reprate         = attr.ib(default=80e6, validator=instance_of(float))
    x_pixels        = attr.ib(default=512, validator=instance_of(int))
    y_pixels        = attr.ib(default=512, validator=instance_of(int))
    z_pixels        = attr.ib(default=1, validator=instance_of(int))
    name            = attr.ib(default='Movie', validator=instance_of(str),
                              convert=trunc_end_of_file)
    binwidth        = attr.ib(default=800e-12, validator=instance_of(float))
    fill_frac       = attr.ib(default=80.0, validator=instance_of(float))
    big_tiff        = attr.ib(default=True, validator=instance_of(bool))
    bidir           = attr.ib(default=True, validator=instance_of(bool))
    num_of_channels = attr.ib(default=1, validator=instance_of(int))
    outputs         = attr.ib(default={}, validator=instance_of(dict))
    censor          = attr.ib(default=False, validator=instance_of(bool))
    flim            = attr.ib(default=False, validator=instance_of(bool))
    lst_metadata    = attr.ib(default={}, validator=instance_of(dict))
    exp_params      = attr.ib(default={}, validator=instance_of(dict))
    line_delta      = attr.ib(default=158000, validator=instance_of(int))
    use_sweeps      = attr.ib(default=False, validator=instance_of(bool))
    cache_size      = attr.ib(default=10*1024**3, validator=instance_of(int))
    tag_as_phase    = attr.ib(default=True, validator=instance_of(bool))
    tag_freq        = attr.ib(default=189e3, validator=instance_of(float))
    summed_mem      = attr.ib(init=False)
    stack           = attr.ib(init=False)
    summed_to_file  = attr.ib(init=False)
    all_tif_ptr     = attr.ib(init=False)

    @property
    def bins_bet_pulses(self) -> int:
        if self.flim:
            return int(np.ceil(1 / (self.reprate * self.binwidth)))
        else:
            return 1

    @property
    def list_of_volume_times(self) -> List[np.uint64]:
        """ All volumes start-times in the movie. """

        volume_times = np.unique(self.data.index.get_level_values('Frames')).astype(np.uint64)
        if len(volume_times) > 1:
            diff_between_frames = np.median(np.diff(volume_times))
        else:
            diff_between_frames = np.uint64(np.max(self.data['time_rel_frames']))

        volume_times = list(volume_times)
        volume_times.append(np.uint64(volume_times[-1] + diff_between_frames))

        return volume_times

    @property
    def photons_per_pulse(self) -> Dict[int, float]:
        """ Caclculate the amount of detected photons per pulse """
        max_time = self.list_of_volume_times[-1] * self.binwidth
        num_of_pulses = int(max_time * self.reprate)
        photons_per_pulse = {}
        if self.num_of_channels == 1:
            photons_per_pulse[1] = self.data.shape[0] / num_of_pulses
            return photons_per_pulse
        else:
            for chan in range(self.num_of_channels):
                photons_per_pulse[chan] = self.data.loc[chan]

    def run(self):
        """
        Main pipeline for the movie object
        :return:
        """
        self.__create_outputs()
        self.__print_outputs()
        print("Movie object created, analysis done.")

    def gen_of_volumes(self, channel_num: int) -> Iterator:
        """
        Populate the deque containing the volumes as a generator.
        Creates a list for each channel in the data. Channels start with 1.
        """

        list_of_frames: List[int] = self.list_of_volume_times  # saves a bit of computation
        for idx, current_time in enumerate(list_of_frames[:-1]):  # populate deque with frames
            cur_data = self.data.xs(key=(current_time, channel_num), level=('Frames', 'Channel'), drop_level=False)
            if not cur_data.empty:
                yield Volume(data=cur_data, x_pixels=self.x_pixels, y_pixels=self.y_pixels,
                             z_pixels=self.z_pixels, number=idx, abs_start_time=current_time,
                             reprate=self.reprate, binwidth=self.binwidth, empty=False,
                             end_time=(list_of_frames[idx + 1] - list_of_frames[idx]),
                             bidir=self.bidir, fill_frac=self.fill_frac, censor=self.censor,
                             line_delta=self.line_delta, use_sweeps=self.use_sweeps,
                             tag_as_phase=self.tag_as_phase, tag_freq=self.tag_freq)
            else:
                yield Volume(data=cur_data, x_pixels=self.x_pixels,
                             y_pixels=self.y_pixels, z_pixels=self.z_pixels, number=idx,
                             reprate=self.reprate, binwidth=self.binwidth, empty=True,
                             end_time=(list_of_frames[idx + 1] - list_of_frames[idx]),
                             bidir=self.bidir, fill_frac=self.fill_frac, censor=self.censor,
                             line_delta=self.line_delta, use_sweeps=self.use_sweeps,
                             tag_as_phase=self.tag_as_phase, tag_freq=self.tag_freq)

    def __create_outputs(self) -> None:
        """
        Create the outputs according to the outputs dictionary.
        Data is generated by appending to a list the needed micro-function to be executed.
        """

        if not self.outputs:
            warnings.warn("No outputs requested. Data is still accessible using the dataframe variable.")
            return
        # Lists that will contain function handles to execute
        funcs_to_execute_during = []
        funcs_to_execute_end = []

        if 'memory' in self.outputs:
            self.summed_mem = {i: 0 for i in range(1, self.num_of_channels + 1)}
            self.stack = {i: deque() for i in range(1, self.num_of_channels + 1)}
            funcs_to_execute_during.append(self.__create_memory_output)
            funcs_to_execute_end.append(self.__convert_deque_to_arr)
            if 'stack' in self.outputs:
                funcs_to_execute_end.append(self.__save_stack_at_once)
            if 'summed' in self.outputs:
                funcs_to_execute_end.append(self.__save_summed_at_once)

        else:
            if 'stack' in self.outputs:
                self.outputs['stack'] = h5py_cache.File(f'{self.outputs["filename"]}', 'a',
                                                        chunk_cache_mem_size=self.cache_size,
                                                        libver='latest', w0=1).require_group('Full Stack')
                funcs_to_execute_during.append(self.__save_stack_incr)
                funcs_to_execute_end.append(self.__close_file)

            if 'summed' in self.outputs:
                self.summed_mem = {i: 0 for i in range(1, self.num_of_channels + 1)}
                funcs_to_execute_during.append(self.__append_summed_data)
                funcs_to_execute_end.append(self.__save_summed_at_once)

        VolTuple = namedtuple('VolumeHist', ('hist', 'edges'))
        data_of_vol = VolTuple

        # Actual body of function - execute the appended functions after generating each volume
        for chan in range(1, self.num_of_channels + 1):
            tq = tqdm(total=len(self.list_of_volume_times)-1,
                      desc=f"Processing volumes in channel {chan} / {self.num_of_channels}",
                      unit="volume", leave=False)
            for idx, vol in enumerate(self.gen_of_volumes(channel_num=chan)):
                data_of_vol.hist, data_of_vol.edges = vol.create_hist()
                for func in funcs_to_execute_during:
                    func(data=data_of_vol.hist, channel=chan, vol_num=idx)
                tq.update(1)
            tq.close()

        for func in funcs_to_execute_end:
            func()

    def __save_stack_at_once(self):
        """ Save the entire in-memory stack into .hdf5 file """
        with h5py_cache.File(f'{self.outputs["filename"]}', 'a', chunk_cache_mem_size=self.cache_size,
                             libver='latest', w0=1) as f:
            print("Saving full stack to disk...")
            for channel in range(1, self.num_of_channels + 1):
                f["Full Stack"][f"Channel {channel}"][...] = self.stack[channel]

    def __save_summed_at_once(self):
        """ Save the netire in-memory summed data into .hdf5 file """
        with h5py_cache.File(f'{self.outputs["filename"]}', 'a', chunk_cache_mem_size=self.cache_size,
                             libver='latest', w0=1) as f:
            for channel in range(1, self.num_of_channels + 1):
                f["Summed Stack"][f"Channel {channel}"][...] = np.squeeze(self.summed_mem[channel])

    def __close_file(self):
        """ Close the file pointer of the specific channel """
        self.outputs['stack'].file.close()

    def __convert_deque_to_arr(self):
        """ Convert a deque with a bunch of frames into a single numpy array with an extra
        dimension (0) containing the data.
        """
        for channel in range(1, self.num_of_channels + 1):
            self.stack[channel] = np.squeeze(np.stack(self.stack[channel], axis=0))

    def __create_memory_output(self, data: np.ndarray, channel: int, **kwargs):
        """
        If the user desired, create two memory constructs -
        A summed array of all images (for a specific channel), and a stack containing
        all images in a serial manner.
        :param data: Data to be saved.
        :param channel: Current spectral channel of data
        """
        self.stack[channel].append(data)
        self.summed_mem[channel] += np.uint16(data)

    def __save_stack_incr(self, data: np.ndarray, channel: int, vol_num: int):
        """
        Save incrementally new data to an open file on the disk
        :param data: Data to save
        :param channel: Current spectral channel of data
        :param vol_num: Current volume
        """
        self.outputs['stack'][f'Channel {channel}'][vol_num, ...] = np.squeeze(data)

    def __append_summed_data(self, data: np.ndarray, channel: int, **kwargs):
        """
        Create a summed variable later to be saved as the channel's data
        :param data: Data to be saved
        :param channel: Spectral channel of data to be saved
        """
        self.summed_mem[channel] += np.uint16(data)

    def __print_outputs(self) -> None:
        """
        Print to console the outputs that were generated.
        """
        if not self.outputs:
            return

        print('======================================================= \nOutputs:\n--------')
        if 'stack' in self.outputs:
            print(f'Stack file created with name "{self.outputs["filename"]}", \ncontaining a data group named'
                  ' "Full Stack", with one dataset per channel.')

        if 'memory' in self.outputs:
            print('The full data is present in dictionary form (key per channel) under `movie.stack`, '
                  'and in stacked form under `movie.summed_mem`.')

        if 'summed' in self.outputs:
            print(f'Summed stack file created with name "{self.outputs["filename"]}", \ncontaining a data group named'
                  ' "Summed Stack", with one dataset per channel.')

    def __nano_flim(self, data: np.ndarray) -> None:
        pass

    def show_summed(self, channel: int=1) -> None:
        """ Show the summed Movie """

        plt.figure()
        try:
            num_of_dims = len(self.summed_mem[channel].shape)
            if num_of_dims > 2:
                plt.imshow(np.sum(self.summed_mem[channel], axis=-(num_of_dims-2)),
                           cmap='gray')
            else:
                plt.imshow(self.summed_mem[channel], cmap='gray')
        except:
            warnings.warn("Can't show summed image when memory output wasn't asked for.")

        plt.title(f'Channel number {channel}')
        plt.axis('off')

    def show_stack(self, channel: int=1, slice_range: Iterable=range(10)) -> None:
        """ Show the stack of given slices """
        if 'time_rel_pulse' in self.data.columns:
            self.__show_stack_flim(channel=channel, slice_range=slice_range)
        else:
            self.__show_stack_no_flim(channel=channel, slice_range=slice_range)

    def __show_stack_no_flim(self, channel: int, slice_range: Iterable):
        """ Show the slices from the generated stack """

        img = None
        for frame in slice_range:
            print(frame, channel)
            if None == img:
                img = plt.imshow(self.stack[channel][frame, :, :], cmap='gray')
            else:
                img.set_data(self.stack[channel][frame, :, :])
            plt.pause(0.1)
            plt.draw()

    def __show_stack_flim(self, channel: int, slice_range: Iterable):
        """ Show the slices from the generated stack that contains FLIM data """

        for frame in slice_range:
            plt.figure()
            plt.imshow(np.sum(self.stack[channel][frame, :, :], axis=-1), cmap='gray')


@attr.s(slots=True)
class Volume(object):
    """
    A Movie() is a sequence of Volumes(). Each volume contains frames in a plane.
    """
    data           = attr.ib(validator=instance_of(pd.DataFrame))
    x_pixels       = attr.ib(default=512, validator=instance_of(int))
    y_pixels       = attr.ib(default=512, validator=instance_of(int))
    z_pixels       = attr.ib(default=1, validator=instance_of(int))
    number         = attr.ib(default=1, validator=instance_of(int))  # the volume's ordinal number
    reprate        = attr.ib(default=80e6, validator=instance_of(float))  # laser repetition rate, relevant for FLIM
    end_time       = attr.ib(default=np.uint64(100), validator=instance_of(np.uint64))
    binwidth       = attr.ib(default=800e-12, validator=instance_of(float))
    bidir          = attr.ib(default=False, validator=instance_of(bool))  # Bi-directional scanning
    fill_frac      = attr.ib(default=80.0, validator=instance_of(float))
    abs_start_time = attr.ib(default=np.uint64(0), validator=instance_of(np.uint64))
    empty          = attr.ib(default=False, validator=instance_of(bool))
    censor         = attr.ib(default=False, validator=instance_of(bool))
    line_delta     = attr.ib(default=158000, validator=instance_of(int))
    use_sweeps     = attr.ib(default=False, validator=instance_of(bool))
    tag_as_phase   = attr.ib(default=True, validator=instance_of(bool))
    tag_freq       = attr.ib(default=189e3, validator=instance_of(float))

    @property
    def metadata(self) -> OrderedDict:
        """
        Creates the metadata of the volume to be created, to be used for creating the actual images
        using histograms. Metadata can include the first photon arrival time, start and end of volume, etc.
        :return: Dictionary of all needed metadata.
        """

        metadata = OrderedDict()
        jitter = 0.02  # 2% of jitter of the signals that creates volumes

        # Volume metadata - rows
        volume_start: int = 0
        metadata['Volume'] = Struct(start=volume_start, end=self.end_time, num=self.x_pixels+1)

        # y-axis metadata - columns
        y_start, y_end = metadata_ydata(data=self.data, jitter=jitter, bidir=self.bidir,
                                        fill_frac=self.fill_frac, delta=self.line_delta,
                                        sweeps=self.use_sweeps)
        if y_end == 1:  # single pixel in frame
            metadata['Y'] = Struct(start=y_start, end=self.end_time, num=self.y_pixels + 1)
        else:
            metadata['Y'] = Struct(start=y_start, end=y_end, num=self.y_pixels + 1)

        # z-axis metadata
        if 'Phase' in self.data.columns:
            z_start = -1 if self.tag_as_phase else 0
            z_end = 1 if self.tag_as_phase else self.tag_period
            metadata['Z'] = Struct(start=z_start, end=z_end, num=self.z_pixels + 1)

        # Laser pulses metadata
        if 'time_rel_pulse' in self.data.columns:
            try:
                laser_start = 0
                laser_end = np.ceil(1 / (self.reprate * self.binwidth)).astype(np.uint8)
                metadata['Laser'] = Struct(start=laser_start, end=laser_end, num=laser_end + 1)
            except ZeroDivisionError:
                laser_start = 0
                warnings.warn('No laser reprate provided. Assuming 80.3 MHz.')
                laser_end = np.ceil(1 / (80.3e6 * self.binwidth)).astype(np.uint8)
                metadata['Laser'] = Struct(start=laser_start, end=laser_end, num=laser_end + 1)

        return metadata

    @property
    def tag_period(self):
        return int(np.ceil(1 / (self.tag_freq * self.binwidth)))

    def __create_hist_edges(self):
        """
        Create three vectors that will create the grid of the frame. Uses Numba internal function for optimization.
        :return: Tuple of np.array
        """
        metadata = self.metadata
        list_of_edges = []

        if self.empty is not True:
            for num_of_dims, key in enumerate(metadata, 1):
                if 'Volume' == key:
                    list_of_edges.append(self.__create_line_array())
                else:
                    list_of_edges.append(create_linspace(start=metadata[key].start,
                                                         stop=metadata[key].end,
                                                         num=metadata[key].num))

            return list_of_edges, num_of_dims
        else:
            return list(np.ones(len(metadata)))

    def __create_line_array(self):
        """
        Generates the edges of the final histogram using the line signal from the data
        :return: np.array
        """
        lines = np.unique(self.data.index.get_level_values('Lines').values) - self.abs_start_time
        lines.sort()
        num_of_lines = len(lines)
        ALLOWED_THRESHOLD = 0.05  # percent
        if num_of_lines > 1:
            if np.abs(1 - (num_of_lines / self.x_pixels)) > ALLOWED_THRESHOLD:  # line signal was too corrupt in the volume
                if num_of_lines >= self.x_pixels:
                    mean_diff = np.diff(lines).mean()
                    return np.r_[
                        lines[:self.x_pixels], np.array([lines[self.x_pixels - 1] + mean_diff], dtype=np.uint64)]

                warnings.warn(f'\nNon-matching number of line events in volume number {self.number}.\n'
                              f'{num_of_lines} lines were recorded, while {self.x_pixels} were required.')
                self.empty = True

            else:  # lines signal is corrupt, but we can save it
                lines = self.__rectify_line_sig(pd.Series(lines))
                return lines

        else:  # single pixel frames, perhaps
            return np.r_[lines, lines + self.end_time]

    def __rectify_line_sig(self, lines: pd.Series) -> np.ndarray:
        """
        Rectify a semi-broken line signal.
        :return: Rectified lines
        """
        delta = self.x_pixels - len(lines)
        CHANGE_DIFF = 0.05  # percent
        diffs = lines.diff()
        mean_val = diffs.mean()
        rel_idx = np.where(diffs.pct_change(periods=1) > CHANGE_DIFF)[0]
        if len(lines)-1 in rel_idx:  # last lines are missing
            needed_lines = 1 + (self.x_pixels+1 - (len(lines)+len(rel_idx)))
            lines = lines[:-1].append(pd.Series(np.linspace(start=lines.iloc[-2] + mean_val,
                                                            stop=lines.iloc[-2]+((needed_lines+1) * mean_val),
                                                            num=needed_lines, dtype=np.uint64)))
            rel_idx = rel_idx[rel_idx != len(diffs)-1]
        if np.abs((diffs.iloc[1] - mean_val) / mean_val) > CHANGE_DIFF:  # first line came late
            rel_idx = np.r_[rel_idx, 1]
        if len(rel_idx) > 0:
            for val in rel_idx:
                missing_lines = int(np.around(diffs[val] / mean_val)) - 1
                lines = lines.append(pd.Series(np.linspace(start=lines.iloc[val - 1] + mean_val,
                                                           stop=lines.iloc[val], endpoint=False,
                                                           num=missing_lines, dtype=np.uint64)))

        if len(lines) != self.x_pixels:  # lines weren't recorded from the get-go
            if lines.iloc[0] == 0:  # we'll append at the end
                lines = lines.sort_values().reset_index(drop=True)
                needed_lines = np.abs(self.x_pixels - len(lines))
                lines = lines.append(pd.Series(np.linspace(start=lines.iloc[-1] + mean_val,
                                                           stop=lines.iloc[-1] + (needed_lines + 1) * mean_val,
                                                           endpoint=False,
                                                           num=needed_lines, dtype=np.uint64)))
            else:
                lines = lines.append(pd.Series(np.linspace(start=1, stop=lines.iloc[0], endpoint=False,
                                                           num=np.abs(self.x_pixels - len(lines)), dtype=np.uint64)))
        lines = lines.sort_values().reset_index(drop=True)
        lines = np.r_[lines.iloc[:self.x_pixels], np.array([lines.iloc[self.x_pixels - 1] + mean_val],
                                                           dtype=np.uint64)]
        return lines

    def create_hist(self) -> Tuple[np.ndarray, Iterable]:
        """
        Create the histogram of data using calculated edges.
        :return: np.ndarray of shape [num_of_cols, num_of_rows] with the histogram data, and edges
        """

        list_of_data_columns = []
        list_of_edges, num_of_dims = self.__create_hist_edges()
        if not self.empty:
            list_of_data_columns.append(self.data['time_rel_frames'].values)
            list_of_data_columns.append(self.data['time_rel_line'].values)
            try:
                list_of_data_columns.append(self.data['Phase'].values)
            except KeyError:
                pass
            try:
                list_of_data_columns.append(self.data['time_rel_pulse'].values)
            except KeyError:
                pass

            data_to_be_hist = np.reshape(list_of_data_columns, (num_of_dims, self.data.shape[0])).T

            assert data_to_be_hist.shape[0] == self.data.shape[0]
            assert len(list_of_data_columns) == data_to_be_hist.shape[1]

            hist, edges = np.histogramdd(sample=data_to_be_hist, bins=list_of_edges)
            if self.bidir:
                hist[1::2] = np.fliplr(hist[1::2])
            if self.censor:
                hist = self.__censor_correction(hist)

            return np.uint8(hist), edges
        else:
            return np.zeros((self.x_pixels, self.y_pixels, self.z_pixels), dtype=np.uint8), (0, 0, 0)

    def create_tag_bins(self) -> np.ndarray:
        pass

    def __censor_correction(self, data) -> np.ndarray:
        """
        Add censor correction to the data after being histogrammed
        :param data:
        :return:
        """
        rel_idx = np.argwhere(np.sum(data, axis=-1) > 1)
        split = np.split(rel_idx, 2, axis=1)
        squeezed = np.squeeze(data[split[0], split[1], :])
        return data


def validate_number_larger_than_zero(instance, attribute, value: int=0):
    """
    Validator for attrs module - makes sure line numbers and row numbers are larger than 0.
    """

    if value >= instance.attribute:
        raise ValueError(f"{attribute} has to be larger than {value}.")


@jit((float64[:](int64, uint64, uint64)), nopython=True, cache=True)
def create_linspace(start, stop, num):
    linspaces = np.linspace(start, stop, num)
    assert np.all(np.diff(linspaces) > 0)
    return linspaces


def metadata_ydata(data: pd.DataFrame, jitter: float=0.02, bidir: bool=True, fill_frac: float=0,
                   delta: int=158000, sweeps: bool=False):
    """
    Create the metadata for the y-axis.

    """
    lines_start: int = 0

    unique_indices: np.ndarray = np.unique(data.index.get_level_values('Lines'))
    if unique_indices.shape[0] <= 1:
        lines_end = 1
        return lines_start, lines_end

    # Case where it's a unidirectional scan and we dump back-phase photons
    if not bidir:
        delta /= 2

    if fill_frac > 0:
        lines_end = delta * fill_frac/100
    else:
        lines_end = delta

    return lines_start, int(lines_end)


@attr.s
class Struct(object):
    """ Basic struct-like object for data keeping. """

    start = attr.ib()
    end = attr.ib()
    num = attr.ib(default=None)
