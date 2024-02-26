import re
import json
import numpy as np
import xml.etree.ElementTree as ET


def QCM_310(file_path : str) -> tuple[list, list, list, list, list, list]:
    """
    Function Details
    ================
    Parameters
    ----------
    file_path: string
        Path to input file.

    Returns
    -------
    sum_times, processes, rates, deviations, thicks, powers, sum_thicks: list
        The total run time, process description, rate, standard deviation,
        measured deposition thickness, and evaporator power for the total length
        of all deposited layers. Note that the time is in seconds.

    Data Types
    ----------
    sum_times, rates, deviations, thicks, powers, sum_thicks: list[float]
    processes: list[string]

    See Also
    --------
    re.compile
    QCM_segment

    Notes
    -----
    Line Patterns:
        The start, end, and data patterns look for "like" lines within the file,
        this is used to distinguish between the separate portions of the file as
        the QCM will reset for different layers.

    The start and end patterns:
        r'Start:   Date: (\d{2}/\d{2}/\d{4})   Time: (\d{2}:\d{2}:\d{2})'. \d
        matches any decimal digit, and the {x} indicates an expected number of
        digits that follow. The end pattern looks much the same, but with r'End'
        in the beginning.

    The data pattern:
        The data pattern that I found works the best is r'(\d+\.\d+),\s+([^,]+)
        \s+([\s\S]+\d+\.\d+)'. This looks first for a digit with a decimal, this
        matches the time, and then it looks for some white space and any other
        characters that follow. It is looking for the deposition phase name. The
        string matching then pulls in the remainder of the line, because there
        is an issue when the rate, or thickness, or any other parameter goes
        negative. It is then easier to just split the "sensor data" on a comma
        delimiter. The data pattern match had to be changed to accommodate white
        space between the process description entry which meant it was tough to
        include the individual sensor data pattern.

    count:
        For depositions of multiple layers, the count is used to correct the
        time stamp index when the re.compile finds lines containing data.

    time correct:
        Every time the evaporator starts a new layer, it will reset the layer
        timer. Plotting then becomes a nightmare as all layers will appear on
        top of one another. To continue the run time counter, the layers are
        indexed and then used to add the previous total time to the new layer
        timer.

        This is done by first finding how many "segments" there are, i.e., how
        many layers there are. This is indicated by the number of times "start"
        appears in the line and then this is used to split the run times into
        the multiple lists.

        For the first segment, the individual run times are the total run time,
        but then the maximum run time of the previous section needs to be added
        to the new run times. As each layer is appended, the maximum run time
        is the total run time of the layers completed.

        The same principle is applied to the layer thickness to calculate a
        total deposition thickness.

    thickness corrections:
        The QCM 310 reads thickness in kA, which is 1000 A, or 100nm. The code
        converts straight to nm when it reads in the data.

    rate corrections:
        The QCM 310 reads rate in A/s, the code converts this to nm/s.

    time conversion:
        The time is converted from seconds to minutes.

    Example
    -------
    >>> file_path = "/Path/To/File.txt"
    >>> t, d, r, std, th, p, sum_th = QCM_310(file_path=file_path)
    >>> t
    [1.2, 2.3, 3.5, 4.6, 5.8, ..., 5688.5, 5689.6]
    >>> d
    ['PreCondition', 'PreCondition', 'PreCondition', 'PreCondition',
    'PreCondition', ..., 'Idle Ramp', 'Idle Ramp']

    ----------------------------------------------------------------------------
    Update History
    ==============

    21/02/2024
    ----------
    Updated from previous repository for current data processing techniques.

    23/02/2024
    ----------
    Complete overhaul of the old function to include pattern matching of the
    lines and handle the data as lists instead of appending each line and split
    etc.

    """

    """ Set the patterns """
    start_pattern = re.compile(
        r'Start:   Date: (\d{2}/\d{2}/\d{4})   Time: (\d{2}:\d{2}:\d{2})')
    data_pattern = re.compile(r'(\d+\.\d+),\s+([^,]+),\s+([\s\S]+\d+\.\d+)')

    """ Initialise variables """
    run_times = []
    processes = []
    rates = []
    deviations = []
    thicks = []
    powers = []
    layer_indices = []

    """ The count is for depositions of multiple layers """
    count = 0

    """ Read the file and extract information """
    with open(file_path, 'r') as in_file:
        file_content = in_file.readlines()

        """ Loop lines and pattern match """
        for index, line in enumerate(file_content):
            start_match = start_pattern.match(line)
            data_match = data_pattern.match(line)

            """ Start match for layer indices """
            if start_match:
                layer_indices.append(index - (count * 4))
                count += 1

            """ Data match and variable append """
            if data_match:
                run_times.append(float(data_match.group(1)) / 60)
                processes.append(f'{data_match.group(2)}')
                sensor_data = data_match.group(3).split(',')
                rates.append(float(sensor_data[0]) / 10)
                deviations.append(float(sensor_data[1]))
                thicks.append(float(sensor_data[2]) * 100)
                powers.append(float(sensor_data[3]))

    """ Find multiple segments """
    times_segments = QCM_segment(
        layer_indices=layer_indices,
        data_array=run_times)
    thickness_segments = QCM_segment(
        layer_indices=layer_indices,
        data_array=thicks)

    """ Correct multiple layer run times """
    sum_times = QCM_adjustments(
        segments=times_segments,
        precision=1)
    sum_thick = QCM_adjustments(
        segments=thickness_segments,
        precision=3)

    return sum_times, processes, rates, deviations, thicks, powers, sum_thick


def QCM_adjustments(segments : tuple[list, ...],
                    precision : int):
    """
    Function Details
    ================
    Create a summation of a segmented list that resets in each segment.

    Parameters
    ----------
    segments: tuple[list, ...]
        List of lists, where each subsequent list needs to be added
        consecutively.
    precision: int
        Level of precision to round the data.

    Returns
    -------
    adjusted_list: list
        Segmented data where the beginning of each segment adds continuously.

    See Also
    --------
    None

    Notes
    -----

    Example
    -------
    >>> segments = [[1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
    >>> adjusted_list = QCM_adjustments(
            segments=segments,
            precision=1)
    >>> adjusted_list
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    ----------------------------------------------------------------------------
    Update History
    ==============

    23/02/2024
    ----------
    Created.

    """
    adjusted_list = []
    for index, segment in enumerate(segments):
        if index == 0:
            [adjusted_list.append(data) for data in segment]
        else:
            corrected_list = [
                round(data + max(adjusted_list), int(precision))
                for data in segment]
            [adjusted_list.append(data) for data in corrected_list]
    return adjusted_list


def QCM_segment(layer_indices : list,
                data_array : list) -> tuple[list, ...]:
    """
    Function Details
    ================
    Use segment indices to split QCM data into segmented arrays.

    Parameters
    ----------
    layer_indices, data_array: list
        Points within the data at which a new layer begins, data array to split.

    Returns
    -------
    segments: tuple[list, ...]
        A list containing a layer-wise split of the data array.

    See Also
    --------
    None

    Notes
    -----
    Split data array into a list of length of each layer, and stack in a list
    with the total number of layers.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    23/02/2024
    ----------
    Created.

    """
    segments = []
    for i in range(len(layer_indices)):
        if i == len(layer_indices) - 1:
            segments.append(data_array[layer_indices[i]:])
        else:
            segments.append(data_array[layer_indices[i]: layer_indices[i + 1]])
    return segments


def QCM_160(file_path : str) -> tuple[list, list, list]:
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
    The function converts time from seconds to minutes, thickness from kA to nm,
    and rate from A/s to nm/s.

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

    21/02/2024
    ----------
    Update name to correspond to device name.

    """
    time, thickness, rate = np.genfromtxt(
        fname=file_path,
        delimiter='\t',
        skip_header=2,
        skip_footer=1,
        usecols=(0, 1, 2),
        unpack=True)
    time /= 60
    thickness *= 100
    rate /= 10
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
