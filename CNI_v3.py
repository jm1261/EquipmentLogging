import numpy as np
import src.fileIO as io
import src.filepaths as fp
import src.plotting as plot

from pathlib import Path


def CNI_log(file_path : str,
            out_path : str,
            plot_dict : dict) -> tuple[str, list]:
    """
    Pull in xml log file from CNI v3 nanoimprint tool.

    Plots log file data as a figure, pulls in recipe, and outputs details.

    Parameters
    ----------
    file_path, out_path: string
        Path to infile, path to outfile.
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
    log_out: list
        List containing the recipe name, recipe steps, and recipe notes.

    See Also
    --------
    get_filename
    load_CNI_xml
    CNI_datatable
    CNI_steps
    CNIplot

    Notes
    -----
    None

    Example
    -------
    None

    """
    file_name = fp.get_filename(file_path=file_path)
    xml_content = io.load_CNI_xml(file_path=file_path)
    _, data = io.CNI_datatable(xml_content=xml_content)
    name, steps, notes = io.CNI_steps(xml_content=xml_content)
    step_string = ' <br> '.join(steps)
    log_out = np.array([name, step_string, notes])
    file_out = Path(f'{out_path}/{file_name}_log.png')
    if file_out.is_file():
        pass
    else:
        plot.CNIplot(
            data=data,
            out_path=file_out,
            plot_dict=plot_dict)
    return file_out, log_out


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
    log_params = {"log_details": []}
    for file in files:
        file_path = Path(f'{data_path}/{file}')
        log_outpath, log_details = CNI_log(
            file_path=file_path,
            out_path=data_path,
            plot_dict=log_dict)
        graph_paths["out_paths"].append(f'{log_outpath}')
        log_params["log_details"].append([detail for detail in log_details])
    out_dict = dict(
        log_dict,
        **graph_paths,
        **log_params)
    io.save_json_dicts(
        out_path=Path(f'{root}/../EquipmentLogging/log_dictionary.json'),
        dictionary=out_dict)
