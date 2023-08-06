"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = Hagai Hargil
Created on Thu Oct 13 09:37:02 2016
"""
import pandas as pd
import warnings


def main_data_readout(gui):
    """
    Main function that reads the lst file and processes its data.
    """
    from pysight.fileIO_tools import FileIO
    from pysight.tabulation_tools import Tabulate
    from pysight.allocation_tools import Allocate
    from pysight.movie_tools import Movie
    from pysight import timepatch_switch
    from pysight.output_tools import OutputParser
    from pysight.gating_tools import GatedDetection
    from pysight.photon_df_tools import PhotonDF
    from pysight.tag_bits_tools import ParseTAGBits
    from pysight.distribute_data import DistributeData
    from pysight.validation_tools import SignalValidator
    import numpy as np

    # Read the file
    cur_file = FileIO(filename=gui.filename, debug=gui.debug, input_start=gui.input_start,
                      input_stop1=gui.input_stop1, input_stop2=gui.input_stop2, binwidth=gui.binwidth,
                      use_sweeps=gui.sweeps_as_lines)
    cur_file.run()

    # Create input structures
    dict_of_slices_hex = timepatch_switch.ChoiceManagerHex().process(cur_file.timepatch)
    # dict_of_slices_bin = timepatch_switch.ChoiceManagerBinary().process(cur_file.timepatch)  # Not supported

    # Process events into dataframe
    tabulated_data = Tabulate(data_range=cur_file.data_range, data=cur_file.data,
                              dict_of_inputs=cur_file.dict_of_input_channels,
                              is_binary=cur_file.is_binary, use_tag_bits=gui.tag_bits,
                              dict_of_slices_hex=dict_of_slices_hex, dict_of_slices_bin=None,
                              time_after_sweep=cur_file.time_after, acq_delay=cur_file.acq_delay,
                              num_of_channels=cur_file.num_of_channels, )
    tabulated_data.run()

    separated_data = DistributeData(df=tabulated_data.df_after_timepatch,
                                    dict_of_inputs=tabulated_data.dict_of_inputs,
                                    use_tag_bits=gui.tag_bits, )
    separated_data.run()

    validated_data = SignalValidator(dict_of_data=separated_data.dict_of_data, num_of_frames=gui.num_of_frames,
                                    binwidth=float(gui.binwidth), use_sweeps=gui.sweeps_as_lines,
                                    delay_between_frames=float(gui.frame_delay),
                                    data_to_grab=separated_data.data_to_grab, line_freq=gui.line_freq,
                                    num_of_lines=gui.x_pixels, bidir=gui.bidir,
                                    bidir_phase=gui.phase, image_soft=gui.imaging_software,
                                    )

    validated_data.run()

    photon_df = PhotonDF(dict_of_data=validated_data.dict_of_data)
    tag_bit_parser = ParseTAGBits(dict_of_data=validated_data.dict_of_data, photons=photon_df.gen_df(),
                                  use_tag_bits=gui.tag_bits, bits_dict=gui.tag_bits_dict)

    analyzed_struct = Allocate(dict_of_inputs=cur_file.dict_of_input_channels, bidir=gui.bidir,
                               laser_freq=float(gui.reprate), binwidth=float(gui.binwidth),
                               tag_pulses=int(gui.tag_pulses), phase=gui.phase,
                               keep_unidir=gui.keep_unidir, flim=gui.flim,
                               censor=gui.censor, dict_of_data=validated_data.dict_of_data,
                               df_photons=tag_bit_parser.gen_df(), num_of_channels=tabulated_data.num_of_channels,
                               tag_freq=float(gui.tag_freq), tag_to_phase=True, tag_offset=gui.tag_offset)
    analyzed_struct.run()

    # Determine type and shape of wanted outputs, and open the file pointers there
    outputs = OutputParser(num_of_frames=len(np.unique(analyzed_struct.df_photons.index
                                                       .get_level_values('Frames')).astype(np.uint64)),
                           output_dict=gui.outputs, filename=gui.filename,
                           x_pixels=gui.x_pixels, y_pixels=gui.y_pixels,
                           z_pixels=gui.z_pixels if analyzed_struct.tag_interp_ok else 1,
                           num_of_channels=analyzed_struct.num_of_channels, flim=gui.flim,
                           binwidth=gui.binwidth, reprate=gui.reprate,
                           lst_metadata=cur_file.lst_metadata, debug=gui.debug)
    outputs.run()

    if gui.gating:
        gated = GatedDetection(raw=analyzed_struct.df_photons, reprate=gui.reprate,
                               binwidth=gui.binwidth)
        gated.run()

    data_for_movie = gated.data if gui.gating else analyzed_struct.df_photons

    # Create a movie object
    final_movie = Movie(data=data_for_movie, x_pixels=int(gui.x_pixels),
                        y_pixels=int(gui.y_pixels), z_pixels=outputs.z_pixels,
                        reprate=float(gui.reprate), name=gui.filename,
                        binwidth=float(gui.binwidth), bidir=gui.bidir,
                        fill_frac=gui.fill_frac if cur_file.fill_fraction == -1.0 else cur_file.fill_fraction,
                        outputs=outputs.outputs, censor=gui.censor, mirror_phase=gui.phase,
                        lines=analyzed_struct.dict_of_data['Lines'].abs_time,
                        num_of_channels=analyzed_struct.num_of_channels, flim=gui.flim,
                        lst_metadata=cur_file.lst_metadata, exp_params=analyzed_struct.exp_params,
                        line_delta=int(validated_data.line_delta), use_sweeps=gui.sweeps_as_lines,
                        tag_as_phase=True, tag_freq=float(gui.tag_freq), )

    final_movie.run()

    return analyzed_struct.df_photons, final_movie

class GUIClass:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.tag_bits_dict = dict(bits_grp_1_label=entries['bits_grp_1_label'],
                                  bits_grp_2_label=entries['bits_grp_2_label'],
                                  bits_grp_3_label=entries['bits_grp_3_label'])

    @property
    def outputs(self):
        """
        Create a dictionary with the wanted user outputs.
        """
        output = {}

        if True == self.summed: output['summed'] = True
        if True == self.memory: output['memory'] = True
        if True == self.stack: output['stack'] = True

        if 'stack' in output:
            if not 'summed' in output and not 'memory' in output:
                warnings.warn("Performance Warning: Writing data to file might take a long time when the required"
                              " output is only 'Full Stack'.")
        return output

def tkinter_to_object(gui):
    """
    Convert a tkinter instance into a pickable dictionary
    :param gui: GUIApp
    :return: namedtuple
    """
    dic = {key: val.get() for key, val in gui.__dict__.items() if 'Var' in repr(val)}
    return GUIClass(**dic)


def run():
    """
    Run the entire script.
    """
    from pysight.tkinter_gui_multiscaler import GUIApp
    from pysight.tkinter_gui_multiscaler import verify_gui_input

    gui = GUIApp()
    gui.root.mainloop()
    verify_gui_input(gui)
    gui_as_object = tkinter_to_object(gui)
    return main_data_readout(gui_as_object)


def run_batch(foldername: str, glob_str: str="*.lst", recursive: bool=False) -> pd.DataFrame:
    """
    Run PySight on all list files in the folder
    :param foldername: str - Main folder to run the analysis on.
    :param glob_str: String for the `glob` function to filter list files
    :param recursive: bool - Whether the search should be recursive.
    :return pd.DataFrame: Record of analyzed data
    """

    import pathlib
    from pysight.tkinter_gui_multiscaler import GUIApp
    from pysight.tkinter_gui_multiscaler import verify_gui_input
    import numpy as np

    path = pathlib.Path(foldername)
    num_of_files = 0
    if not path.exists():
        raise UserWarning(f"Folder {foldername} doesn't exist.")
    if recursive:
        all_lst_files = path.rglob(glob_str)
        print(f"Running PySight on the following files:")
        for file in list(all_lst_files):
            print(str(file))
            num_of_files += 1
        all_lst_files = path.rglob(glob_str)
    else:
        all_lst_files = path.glob(glob_str)
        print(f"Running PySight on the following files:")
        for file in list(all_lst_files):
            print(str(file))
            num_of_files += 1
        all_lst_files = path.glob(glob_str)

    data_columns = ['fname', 'done', 'error']
    data_record = pd.DataFrame(np.zeros((num_of_files, 3)), columns=data_columns)  # store result of PySight
    gui = GUIApp()
    gui.root.mainloop()
    gui.filename.set('.lst')  # no need to choose a list file
    verify_gui_input(gui)
    named_gui = tkinter_to_object(gui)

    try:
        for idx, lst_file in enumerate(all_lst_files):
            named_gui = named_gui._replace(filename=(str(lst_file)))
            data_record.loc[idx, 'fname'] = str(lst_file)
            try:
                main_data_readout(named_gui)
            except BaseException as e:
                print(f"File {str(lst_file)} returned an error. Moving onwards.")
                data_record.loc[idx, 'done'] = False
                data_record.loc[idx, 'error'] = repr(e)
            else:
                data_record.loc[idx, 'done'] = True
                data_record.loc[idx, 'error'] = None
    except TypeError as e:
        print(repr(e))

    print(f"Summary of batch processing:\n{data_record}")
    return data_record


def mp_batch(foldername):
    import pathlib
    from pysight.tkinter_gui_multiscaler import GUIApp
    from pysight.tkinter_gui_multiscaler import verify_gui_input
    import numpy as np
    import multiprocessing as mp

    path = pathlib.Path(foldername)
    glob_str = '*.lst'
    num_of_files = 0
    if not path.exists():
        raise UserWarning(f"Folder {foldername} doesn't exist.")
    all_lst_files = path.glob(glob_str)
    print(f"Running PySight on the following files:")
    for file in list(all_lst_files):
        print(str(file))
        num_of_files += 1
    all_lst_files = path.glob(glob_str)

    data_columns = ['fname', 'done', 'error']
    data_record = pd.DataFrame(np.zeros((num_of_files, 3)), columns=data_columns)  # store result of PySight
    gui = GUIApp()
    gui.root.mainloop()
    gui.filename.set('.lst')  # no need to choose a list file
    verify_gui_input(gui)
    all_guis = []
    for file in all_lst_files:
        g = tkinter_to_object(gui)
        g.filename = str(file)
        all_guis.append(g)
    pool = mp.Pool()
    rec = pool.map(main_data_readout, all_guis)
    return rec


if __name__ == '__main__':
    df, movie = run()
    # dat[a = run_batch(foldername="", glob_str="*.lst", recursive=False)
    # res = mp_batch(r'C:\Users\Hagai\Documents\GitHub\python-pysight')
