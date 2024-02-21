import src.fileIO as io
import src.filepaths as fp
import src.plotting as plot

from pathlib import Path


def sputter_log(file_path : str,
                out_path : str,
                plot_dict : dict) -> str:
    """
    Function Details
    ================
    Pulls in txt log file from the sputterer QCM.

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
    get_filename
    load_sputter_log
    sputterer_plots

    Notes
    -----
    Reads in sputterer log text file and plots average rate and average
    thickness as a function of time, as measured by the QCM. Will only do this
    if the plot has not yet been plotted.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    19/02/2024
    ----------
    Function brought over from old repository and updated for new data
    processing techniques.

    """
    file_name = fp.get_filename(file_path=file_path)
    time, average_thickness, average_rate = io.QCM_160(file_path=file_path)
    file_out = Path(f'{out_path}/{file_name}_log.png')
    if file_out.is_file():
        pass
    else:
        plot.sputterer_plots(
            time=time,
            thickness=average_thickness,
            rate=average_rate,
            plot_dict=plot_dict,
            out_path=file_out)
    return file_out


if __name__ == '__main__':
    '''
    Root setup for notebooks repository as root directory. Remove '..' to run
    from script.
    '''
    root = Path().absolute()
    log_dict = io.load_json(
        file_path=Path(f'{root}/../EquipmentLogging/log_dictionary.json'))
    files = log_dict["data_files"]
    data_path = log_dict["data_path"]
    graph_paths = {"out_paths": []}
    for file in files:
        file_path = Path(f'{data_path}/{file}')
        log_outpath = sputter_log(
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