import json
import numpy as np
import xml.etree.ElementTree as ET


def load_sputter_log(file_path : str) -> tuple[list, list, list]:
    """
    Function Details
    ================
    Reads sputter log text file.

    Loads sputterer txt file from the QCM.

    Parameters
    ----------
    file_path: string
        Path to file.

    Returns
    -------
    time, thickness, rate: list
        Time steps, average thickness, and average rate column from the log.

    See Also
    --------
    genfromtxt

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    19/02/2024
    ----------
    Updated and adapted function from a previous repository for updated data
    processing methods.

    """
    time, thickness, rate = np.genfromtxt(
        fname=file_path,
        delimiter='\t',
        skip_header=2,
        skip_footer=1,
        usecols=(0, 1, 2),
        unpack=True)
    return time, thickness, rate


def load_CNI_xml(file_path : str) -> object:
    """
    Parameters
    ----------
    file_path: string
        Path fo file.

    Returns
    -------
    root: object
        xml element containing all the document.

    See Also
    --------
    None

    Notes
    -----
    The CNI v3.0 software outputs an xml file that has several <div> categories
    in it. To avoid an issue where ElementTree was reading in "useless"
    information, the function wraps the xml string in a <root> tag.

    Example
    -------
    None

    """
    with open(file_path, 'r') as file:
        xml_content = file.read()
        split = xml_content.split('\n')
        split.append('</root>')
        content_split = np.insert(split, 0, '<root>')
        content = '\n'.join(content_split)
        root = ET.fromstring(content)
    return root


def CNI_datatable(xml_content : object) -> list:
    """
    Read CNI v3 data table log and return with column headers and data.

    Parameters
    ----------
    xml_content: object
        xml element containing all the document.

    Returns
    -------
    column_names, return_data: list
        Column headers, data as a 2D numpy array.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    data_points_elements = xml_content.find(".//DataPoints")
    data_points_text = data_points_elements.text.strip()
    data_lines = data_points_text.split('\n')
    column_names = data_lines[0].split('\t')
    data = []
    for line in data_lines[1: ]:
        values = line.split('\t')
        data.append(values[1: ])
    return_data = np.array([np.array(x_i) for x_i in data])
    return column_names, return_data


def CNI_steps(xml_content : object) -> list:
    """
    Read CNI v3 recipe log and return the steps.

    Parameters
    ----------
    xml_content: object
        xml element containing all the document.

    Returns
    -------
    recipe_steps: list
        Recipe steps in a list.
    recipe_name, recipe_notes: string
        Recipe name and recipe notes from xml content.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    recipe_section = xml_content.find(".//Recipe")
    recipe_name = (recipe_section.find(".//name")).text.strip()
    steps = recipe_section.find(".//steps")
    recipe_steps = [
        step_element.text.strip() for step_element in steps.findall(".//step")]
    note_element = recipe_section.find(".//notes")
    recipe_notes = note_element.text.strip()
    return recipe_name, recipe_steps, recipe_notes


def load_json(file_path : str) -> dict:
    """
    Loads .json file types.

    Use json python library to load a .json file.

    Parameters
    ----------
    file_path : string
        Path to file.

    Returns
    -------
    json file : dictionary
        .json dictionary file.

    See Also
    --------
    read_GMR_file
    save_json_dicts

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Examples
    --------
    my_dictionary = load_json(file_path="/Path/To/File")

    """
    with open(file_path, 'r') as file:
        return json.load(file)


def convert(o):
    """
    Check data type.

    Check type of data string.

    Parameters
    ----------
    o : string
        String to check.

    Returns
    -------
    TypeError : Boolean
        TypeError if string is not suitable.


    See Also
    --------
    None.

    Notes
    -----
    None.

    Examples
    --------
    None.

    """
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path : str,
                    dictionary : dict) -> None:
    """
    Save .json file types.

    Use json python library to save a dictionary to a .json file.

    Parameters
    ----------
    out_path : string
        Path to file.
    dictionary : dictionary
        Dictionary to save.
    
    Returns
    -------
    None

    See Also
    --------
    load_json

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Examples
    --------
    save_json_dicts(
        out_path="/Path/To/File",
        dictionary=my_dictionary)

    """
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')