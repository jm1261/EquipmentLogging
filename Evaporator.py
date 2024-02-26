import src.fileIO as io
import src.filepaths as fp
import src.plotting as plot

from pathlib import Path


def evaporator_logs(file_path : str,
                    out_path : str,
                    plot_dict : str) -> str:
    """
    Function Details
    ================
    Pulls in txt log file from the evaporator QCM.

    Plots log file data as a figure.

    Parameters
    ----------
    file_path, out_path: string
        Path to file, path to save.
    plot_dict: dictionary
        Plot settings dictionary, containing:
            {
                "width": plot width,\n
                "height": plot height,\n
                "dpi": dots per square inch,\n
                "grid": True/False,\n
                "legend_loc": legend location,\n
                "legend_col": legend column number,\n
                "legend_size": size of legend text,\n
                "axis_fontsize": font size for axis labels,\n
                "label_size": size for tick labels
            }

    Returns
    -------
    file_out: string
        Path to outfile.

    See Also
    --------
    QCM_310
    get_filename
    evaporator_plot

    Notes
    -----
    Reads in the evaporator log text file and plots the total thickness (can be
    changed), rate, power, and deviation as a function of run time. Will only
    do this if the plot has not yet been plotted.
    To change between total thickness and layer-wise thickness, the QCM_310
    output should be as follows:

    time, process, rate, deviation, thickness, power, total_thickness.

    But this has been changed for PEP8 line spacing, simply remove the final
    variable and replace it with a "_" and change the "_" to thickness for the
    layer-wise thickness plotting.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    26/02/2024
    ----------
    Created.

    """
    file_name = fp.get_filename(file_path=file_path)
    time, processes, rate, deviation, _, power, thickness = io.QCM_310(
        file_path=file_path)
    file_out = Path(f'{out_path}/{file_name}_log.png')
    if file_out.is_file():
        pass
    else:
        plot.evaporator_plot(
            time=time,
            processes=processes,
            thickness=thickness,
            rate=rate,
            deviation=deviation,
            power=power,
            out_path=file_out,
            plot_dict=plot_dict)
    return file_out


if __name__ == '__main__':
    '''
    Root setup for notebooks repository as a root directory. Remove '..' to run
    from script.
    '''
    root = Path().absolute()
    log_dict = io.load_json(
        file_path=Path(f'{root}/../EquipmentLogging/log_dictionary.json'))
    files = log_dict["data_files"]
    data_path = log_dict["data_path"]
    graph_paths = {"out_paths": []}
    for file in files:
        file_path=Path(f'{data_path}/{file}')
        log_outpath = evaporator_logs(
            file_path=file_path,
            out_path=data_path,
            plot_dict=log_dict)
        graph_paths["out_paths"].append(f'{log_outpath}')
    out_dict = dict(
        log_dict,
        **graph_paths)
    io.save_json_dicts(
        out_path=Path(f'{root}/../EquipmentLogging/log_dictionary.json'),
        dictionary=out_dict)
