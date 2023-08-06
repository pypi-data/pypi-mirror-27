"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = Hagai Hargil
Created on Thu Oct 13 09:37:02 2016
"""


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
    import numpy as np

    # Read the file
    cur_file = FileIO(filename=gui.filename.get(), debug=gui.debug.get(), input_start=gui.input_start.get(),
                      input_stop1=gui.input_stop1.get(), input_stop2=gui.input_stop2.get(), binwidth=gui.binwidth.get(),
                      use_sweeps=gui.sweeps_as_lines.get())
    cur_file.run()

    # Create input structures
    dict_of_slices_hex = timepatch_switch.ChoiceManagerHex().process(cur_file.timepatch)
    # dict_of_slices_bin = timepatch_switch.ChoiceManagerBinary().process(cur_file.timepatch)  # Not supported

    # Process events into dataframe
    tabulated_data = Tabulate(timepatch=cur_file.timepatch, data_range=cur_file.data_range,
                              dict_of_inputs=cur_file.dict_of_input_channels, data=cur_file.data,
                              is_binary=cur_file.is_binary, num_of_frames=gui.num_of_frames.get(),
                              laser_freq=float(gui.reprate.get()), binwidth=float(gui.binwidth.get()),
                              dict_of_slices_hex=dict_of_slices_hex, dict_of_slices_bin=None,
                              use_tag_bits=gui.tag_bits.get(), use_sweeps=gui.sweeps_as_lines.get(),
                              time_after_sweep=cur_file.time_after, acq_delay=cur_file.acq_delay,
                              line_freq=gui.line_freq.get(), x_pixels=gui.x_pixels.get(),
                              y_pixels=gui.y_pixels.get(), bidir=gui.bidir.get(),
                              bidir_phase=gui.phase.get(), num_of_channels=cur_file.num_of_channels)
    tabulated_data.run()

    photon_df = PhotonDF(dict_of_data=tabulated_data.dict_of_data)
    tag_bit_parser = ParseTAGBits(dict_of_data=tabulated_data.dict_of_data, photons=photon_df.gen_df(),
                                  use_tag_bits=gui.tag_bits.get(), bits_dict=gui.tag_bits_dict)

    analyzed_struct = Allocate(dict_of_inputs=cur_file.dict_of_input_channels, bidir=gui.bidir.get(),
                               laser_freq=float(gui.reprate.get()), binwidth=float(gui.binwidth.get()),
                               tag_pulses=int(gui.tag_pulses.get()), phase=gui.phase.get(),
                               keep_unidir=gui.keep_unidir.get(), flim=gui.flim.get(),
                               censor=gui.censor.get(), dict_of_data=tabulated_data.dict_of_data,
                               df_photons=tag_bit_parser.gen_df(), num_of_channels=tabulated_data.num_of_channels,
                               tag_freq=float(gui.tag_freq.get()), tag_to_phase=True, tag_offset=gui.tag_offset.get())
    analyzed_struct.run()

    # Determine type and shape of wanted outputs, and open the file pointers there
    outputs = OutputParser(num_of_frames=len(np.unique(analyzed_struct.df_photons.index
                                                       .get_level_values('Frames')).astype(np.uint64)),
                           output_dict=gui.outputs, filename=gui.filename.get(),
                           x_pixels=gui.x_pixels.get(), y_pixels=gui.y_pixels.get(),
                           z_pixels=gui.z_pixels.get() if analyzed_struct.tag_interp_ok else 1,
                           num_of_channels=analyzed_struct.num_of_channels, flim=gui.flim.get(),
                           binwidth=gui.binwidth.get(), reprate=gui.reprate.get(),
                           lst_metadata=cur_file.lst_metadata, debug=gui.debug.get())
    outputs.run()

    if gui.gating.get():
        gated = GatedDetection(raw=analyzed_struct.df_photons, reprate=gui.reprate.get(),
                               binwidth=gui.binwidth.get())
        gated.run()

    data_for_movie = gated.data if gui.gating.get() else analyzed_struct.df_photons

    # Create a movie object
    final_movie = Movie(data=data_for_movie, x_pixels=int(gui.x_pixels.get()),
                        y_pixels=int(gui.y_pixels.get()), z_pixels=outputs.z_pixels,
                        reprate=float(gui.reprate.get()), name=gui.filename.get(),
                        binwidth=float(gui.binwidth.get()), bidir=gui.bidir.get(),
                        fill_frac=gui.fill_frac.get() if cur_file.fill_fraction == -1.0 else cur_file.fill_fraction,
                        outputs=outputs.outputs, censor=gui.censor.get(),
                        num_of_channels=analyzed_struct.num_of_channels, flim=gui.flim.get(),
                        lst_metadata=cur_file.lst_metadata, exp_params=analyzed_struct.exp_params,
                        line_delta=int(tabulated_data.line_delta), use_sweeps=gui.sweeps_as_lines.get(),
                        tag_as_phase=True, tag_freq=float(gui.tag_freq.get()), mirror_phase=gui.phase.get())

    final_movie.run()

    return analyzed_struct.df_photons, final_movie


def run():
    """
    Run the entire script.
    """
    from pysight.tkinter_gui_multiscaler import GUIApp
    from pysight.tkinter_gui_multiscaler import verify_gui_input

    gui = GUIApp()
    gui.root.mainloop()
    verify_gui_input(gui)
    return main_data_readout(gui)


def run_batch(foldername: str, glob_str: str="*.lst", recursive: bool=False):
    """
    Run PySight on all list files in the folder
    :param foldername: str - Main folder to run the analysis on.
    :param glob_str: String for the `glob` function to filter list files
    :param recursive: bool - Whether the search should be recursive.
    :return: None
    """

    import pathlib
    from pysight.tkinter_gui_multiscaler import GUIApp
    from pysight.tkinter_gui_multiscaler import verify_gui_input

    path = pathlib.Path(foldername)
    if not path.exists():
        raise UserWarning(f"Folder {foldername} doesn't exist.")
    if recursive:
        all_lst_files = path.rglob(glob_str)
        print(f"Running PySight on the following files:")
        for file in list(all_lst_files):
            print(str(file))
        all_lst_files = path.rglob(glob_str)
    else:
        all_lst_files = path.glob(glob_str)
        print(f"Running PySight on the following files:")
        for file in list(all_lst_files):
            print(str(file))
        all_lst_files = path.glob(glob_str)

    gui = GUIApp()
    gui.root.mainloop()
    gui.filename.set('.lst')  # no need to choose a list file
    verify_gui_input(gui)

    try:
        for lst_file in all_lst_files:
            gui.filename.set(str(lst_file))
            try:
                main_data_readout(gui)
            except:
                print(f"File {str(lst_file)} returned an error. Moving onwards.")
    except TypeError as e:
        print(e)


if __name__ == '__main__':
    df, movie = run()
    # run_batch(foldername=r"X:\Hagai", glob_str="*.lst", recursive=False)
