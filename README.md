# Equipment Logging

<div style="text-align: justify" >

Data logging software for a variety of nanofabrication equipment, including a nanoimprint tool and quartz crystal microbalance software. The package is directed towards specific equipment logging techniques, and this is clarified in this readme file.

## Contents

* [General Information](#general-information)
* [Package Requirements](#package-requirements)
* [Launch](#launch)
* [Setup](#setup)
  * [File Paths](#file-paths)
  * [Log Dictionary](#log-dictionary)
* [Functions](#functions)

## General Information

QCM and log file plotting software built using Python 3. The code in this repository is deigned to plot the QCM 160 and 310 outputs for a Pulsed DC Magnetron Sputterer and a MB EVAP Electron-Beam Evaporator, whilst also containing a plotter for a CNI v3.0 Nanoimprint Tool.

## Package Requirements

Language and package requirements can also be found in requirements.txt. The code was built using the following languages and module versions:

* Python 3.6-3.10
* numpy 1.21.4
* matplotlib 3.5.0

## Launch

The code can be run from any terminal or editor. Main scripts are in the repository's main directory, while source code is stored safely in /src. The code relies on using a dictionary for plotting and data file path inputs, which should be stored in log_dictionary.json in the main directory. The scripts are set up to use a separate repository as the open workspace in an editor, simply adjust the file paths in the scripts appropriately.

## Setup

The setup information for the repository, file paths, and log dictionary is below. The /src directory should be left alone.

### File paths

Each script contains a file path from the root directory to the repository's main directory. This is given by Path().absolute()/Path/To/Directory. The scripts are set up to be run from a VSCode workspace and can be adjusted depending on the working condition.

### Log Dictionary

The log dictionary contains standard plot settings, data file names, data file path, and out paths (once the code is run). This is how the repository can be controlled from another workspace. The scripts all plot and run depending on the file paths and file names in these fields. Adjust them accordingly.

## Functions

The functions are all well documented, detailing the purpose of each one. For more info, see the scripts.

</div>