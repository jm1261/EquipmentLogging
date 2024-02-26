import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator, ScalarFormatter, MultipleLocator


def cm_to_inches(cm: float) -> float:
    """
    Returns centimeters as inches.

    Uses the conversion rate to convert a value given in centimeters to inches.
    Useful for matplotlib plotting.

    Parameters
    ----------
    cm : float
        Value of the desired figure size in centimeters.

    Returns
    -------
    inches : float
        Value of the desired figure size in inches.

    See Also
    --------
    None

    Notes
    -----
    Conversion rate given to 6 decimal places, but inches rounded to 2 decimal
    places.

    Example
    -------
    >>> cm = 15
    >>> inches = cm_to_inches(cm=cm)
    >>> inches
    5.91

    """
    return round(cm * 0.393701, 2)


def CNIplot(data : list,
            out_path : str,
            plot_dict : dict):
    """
    Plot log parameters for the CNI v3 nanoimprint tool.

    Plots UV power, temperature, pressure, and vacuum parameters.

    Parameters
    ----------
    data: list
        2D data array from the CNI log file.
    out_path: string
        Path to save.
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
    None

    See Also
    --------
    None

    Notes
    -----
    Imitates the plots in the logging software but with greater resolution.

    Example
    -------
    None

    """
    times = [float(x) if x != "NaN" else 0 for x in data[:, 0]]
    TSetP = [float(x) if x != "NaN" else 0 for x in data[:, 1]]
    TMeas = [float(x) if x != "NaN" else 0 for x in data[:, 2]]
    FSetP = [float(x) if x != "NaN" else 0 for x in data[:, 3]]
    FMeas = [float(x) if x != "NaN" else 0 for x in data[:, 4]]
    ICVTh = [float(x) if x != "NaN" else 0 for x in data[:, 5]]
    ICVMe = [float(x) if x != "NaN" else 0 for x in data[:, 6]]
    HMPow = [float(x) if x != "NaN" else 0 for x in data[:, 7]]
    UVPow = [float(x) if x != "NaN" else 0 for x in data[:, 8]]
    UVTem = [float(x) if x != "NaN" else 0 for x in data[:, 9]]
    colors = plt.cm.tab10.colors[:5]
    fig = plt.figure(
        figsize=[
            cm_to_inches(cm=plot_dict["width"]),
            cm_to_inches(cm=plot_dict["height"]) * 2],
        dpi=plot_dict["dpi"])
    grid = plt.GridSpec(
        nrows=2,
        ncols=2)
    ax1 = fig.add_subplot(grid[0, 0:])
    ax2 = ax1.twinx()
    ax3 = fig.add_subplot(grid[1, 0])
    ax4 = fig.add_subplot(grid[1, 1])
    line1 = ax1.plot(
        times,
        TSetP,
        color=colors[0],
        lw=2,
        label='T Set Point')
    line2 = ax1.plot(
        times,
        TMeas,
        color=colors[1],
        lw=2,
        label='T Measured')
    line3 = ax1.plot(
        times,
        UVTem,
        color=colors[2],
        lw=2,
        label='UV Temp')
    line4 = ax2.plot(
        times,
        HMPow,
        color=colors[3],
        lw=2,
        label='HM Power')
    line5 = ax2.plot(
        times,
        UVPow,
        color=colors[4],
        lw=2,
        label='UV Power')
    ax3.plot(
        times,
        FSetP,
        color=colors[0],
        lw=2,
        label='F Set Point')
    ax3.plot(
        times,
        FMeas,
        color=colors[1],
        lw=2,
        label='F Measured')
    ax4.plot(
        times,
        ICVTh,
        color=colors[0],
        lw=2,
        label='Vacuum Threshold')
    ax4.plot(
        times,
        ICVMe,
        color=colors[1],
        lw=2,
        label='Vacuum Measured')
    if plot_dict["grid"] == "True":
        grid = True
        ax1.grid(
            visible=grid,
            alpha=0.5)
        ax3.grid(
            visible=grid,
            alpha=0.5)
        ax4.grid(
            visible=grid,
            alpha=0.5)
    else:
        grid = False
    lines = line1 + line2 + line3 + line4 + line5
    labels = [line.get_label() for line in lines]
    ax1.legend(
        lines,
        labels,
        frameon=True,
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={"size": plot_dict["legend_size"]})
    ax3.legend(
        frameon=True,
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={"size": plot_dict["legend_size"] * 0.75})
    ax4.legend(
        frameon=True,
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={"size": plot_dict["legend_size"] * 0.75})
    ax1.set_xlabel(
        'Time [s]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax1.set_ylabel(
        r'Temperature [$\bf{\degree C}$]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax2.set_ylabel(
        'Power [mW]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        rotation=270,
        labelpad=20)
    ax3.set_xlabel(
        'Time [s]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax3.set_ylabel(
        'Pressure [bar]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax4.set_xlabel(
        'Time [s]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax4.set_ylabel(
        'Vacuum [mbar]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax1.set_title(
        'Exposure Temperature/Power',
        fontsize=plot_dict["title_fontsize"] * 0.75,
        fontweight='bold')
    ax3.set_title(
        'Exposure Pressure',
        fontsize=plot_dict["title_fontsize"] * 0.5,
        fontweight='bold')
    ax4.set_title(
        'Chamber Vacuum',
        fontsize=plot_dict["title_fontsize"] * 0.5,
        fontweight='bold')
    ax4.set_yscale('log') 
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax3.xaxis.set_minor_locator(AutoMinorLocator())
    ax3.yaxis.set_minor_locator(AutoMinorLocator())
    ax4.xaxis.set_minor_locator(AutoMinorLocator())
    ax4.yaxis.set_major_locator(MultipleLocator(200))
    ax4.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax1.tick_params(
        axis='both',
        which='major',
        labelsize=plot_dict["label_size"])
    ax2.tick_params(
        axis='y',
        which='major',
        labelsize=plot_dict["label_size"])
    ax3.tick_params(
        axis='both',
        which='major',
        labelsize=plot_dict["label_size"])
    ax4.tick_params(
        axis='both',
        which='major',
        labelsize=plot_dict["label_size"])
    fig.tight_layout()
    plt.savefig(
        out_path,
        bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)


def sputterer_plots(time : list,
                    thickness : list,
                    rate : list,
                    out_path : str,
                    plot_dict : dict) -> None:
    """
    Function Details
    ================
    Plots sputterer log file.

    Plots thickness and rate as a function of time.

    Parameters
    ----------
    time, thickness, rate: list
        Data for time, thickness, and rate measurements.
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
    out_path: string
        Path to save.

    Returns
    -------
    None

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    20/02/2024
    ----------
    Updated from old repository and adapted for new data processing techniques.

    """
    colors = plt.cm.tab10.colors[:2]
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=plot_dict["width"]),
            cm_to_inches(cm=plot_dict["height"])],
        dpi=plot_dict["dpi"])
    ax2 = ax1.twinx()
    line1 = ax1.plot(
        time,
        thickness,
        color=colors[0],
        lw=2,
        label='Thickness')
    line2 = ax2.plot(
        time,
        rate,
        color=colors[1],
        lw=2,
        label='Rate')
    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax1.legend(
        lines,
        labels,
        frameon=True,
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={"size": plot_dict["legend_size"]})
    ax1.set_xlabel(
        'Time [mins]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax1.set_ylabel(
        'Thickness [nm]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax2.set_ylabel(
        'Rate [nm/s]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax1.set_title(
        'Sputtering Thickness/Rate',
        fontsize=plot_dict["title_fontsize"],
        fontweight='bold')
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.tick_params(
        axis='both',
        which='major',
        labelsize=plot_dict["label_size"])
    ax2.tick_params(
        axis='y',
        which='major',
        labelsize=plot_dict["label_size"])
    plt.savefig(
        out_path,
        bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)


def extract_unique_processes(processes : list) -> tuple[list, list]:
    """
    Function Details
    ================
    Find the transition phases in the evaporator log.

    Parameters
    ----------
    processes: list
        List of all the evaporator processes with time stamp.

    Returns
    -------
    process_indices, unique_processes: list
        List containing the indices at which a transition occurs and the phase
        at those indices.

    See Also
    --------
    None

    Notes
    -----
    None

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


def evaporator_plot(time : list,
                    processes : list,
                    thickness : list,
                    rate : list,
                    deviation : list,
                    power : list,
                    out_path : str,
                    plot_dict : dict) -> None:
    """
    Function Details
    ================
    Plot the electron beam evaporator log file.

    Parameters
    ----------
    time, processes, thickness, rate, deviation, power: list
        Run time, processes, deposition thickness, deposition rate, deposition
        deviation, and deposition power, all from the log file and all of the
        same length.
    out_path: string
        Path to save.
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
    None

    See Also
    --------
    extract_unique_processes

    Notes
    -----
    Unique processes:
        The processes list contains a list of the evaporator steps at every time
        step. This is not necessary to plot, instead the list is used to mark
        the main thickness graph with the transitions in this phase. The indices
        at which these transitions occur is found using the function
        extract_unique_processes

    Axes:
        The evaporator data is a thickness, a rate, a deviation, a power, and a
        list of processes. The thickness is the main priority and has its own
        axes, while the rate, deviation, and power are plotted on a subplot. The
        list of processes is used as an indicator on the main plot. These are
        drawn with grey dotted lines and marked with unique process identifiers.
        The process indicator is offset by a 2/3 or 1/3 y-axis locator to avoid
        the labels crossing over one another.

    Legend:
        The legend can fit outside of the axes due to a triple y-axis on the
        second plot, which allows for a better spread of information across the
        graph.

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

    """ Get the unique processes and indices """
    process_indices, unique_processes = extract_unique_processes(
        processes=processes)

    """ Set up figure """
    colors = plt.cm.tab10.colors[:7]
    fig = plt.figure(
        figsize=[
            cm_to_inches(cm=plot_dict["width"]),
            cm_to_inches(cm=plot_dict["height"]) * 2],
        dpi=plot_dict["dpi"])
    grid = plt.GridSpec(
        nrows=2,
        ncols=1)

    """ Set up axes """
    ax1 = fig.add_subplot(grid[0, 0])
    ax2 = fig.add_subplot(grid[1, 0])
    ax3 = ax2.twinx()
    ax4 = ax2.twinx()
    ax4.spines.right.set_position(('axes', 1.3))

    """ Set up process indicators """
    for index, process_index in enumerate(process_indices):
        ax1.axvline(
            x=time[process_index],
            color='lightgray',
            linestyle='--',
            linewidth=2)
        if index % 2:
            midpoint_y = (max(thickness) + min(thickness) ) / 1.5
        else:
            midpoint_y = (max(thickness) + min(thickness) ) / 3
        ax1.text(
            x=time[process_index],
            y=midpoint_y,
            s=unique_processes[index],
            rotation=270,
            fontsize=5,
            fontweight='bold',
            ha='center',
            va='center')

    """ Data lines """
    line1 = ax1.plot(
        time,
        thickness,
        color=colors[0],
        lw=2,
        label='Thickness')
    line2 = ax2.plot(
        time,
        rate,
        color=colors[2],
        lw=2,
        label='Rate')
    line3 = ax3.plot(
        time,
        deviation,
        color=colors[3],
        lw=2,
        label='Deviation')
    line4 = ax4.plot(
        time,
        power,
        color=colors[4],
        lw=2,
        label='Power')

    """ Grid """
    ax1.grid(
        visible=True,
        alpha=0.5)

    """ Legend """
    lines = line1 + line2 + line3 + line4
    labels = [line.get_label() for line in lines]
    ax1.legend(
        lines,
        labels,
        frameon=True,
        loc='center right',
        bbox_to_anchor=(1.5, 0.5),
        ncol=plot_dict["legend_col"],
        prop={"size": plot_dict["legend_size"] * 0.8})

    """ Labels """
    ax1.set_xlabel(
        'Time [min]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax2.set_xlabel(
        'Time [min]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax1.set_ylabel(
        'Thickness [nm]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax2.set_ylabel(
        'Rate [nm/s]',
        fontsize=plot_dict['axis_fontsize'],
        fontweight='bold')
    ax3.set_ylabel(
        'Deviation [au]',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        rotation=270,
        labelpad=20)
    ax4.set_ylabel(
        'Power [%]',
        fontsize=plot_dict['axis_fontsize'],
        fontweight='bold',
        rotation=270,
        labelpad=20)
    ax1.set_title(
        'Thickness',
        fontsize=plot_dict["title_fontsize"],
        fontweight='bold')
    ax2.set_title(
        'Parameters',
        fontsize=plot_dict["title_fontsize"],
        fontweight='bold')

    """ Ticks """
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax3.yaxis.set_minor_locator(AutoMinorLocator())
    ax4.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.tick_params(
        axis='both',
        which='major',
        labelsize=plot_dict["label_size"])
    ax2.tick_params(
        axis='both',
        which='major',
        labelsize=plot_dict["label_size"])
    ax3.tick_params(
        axis='y',
        which='major',
        labelsize=plot_dict["label_size"])
    ax4.tick_params(
        axis='y',
        which='major',
        labelsize=plot_dict["label_size"])

    """ Save """
    fig.tight_layout()
    plt.savefig(
        out_path,
        bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)
