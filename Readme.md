# PlateReader

A tool to read and plot data from a [Cytation 5](https://www.biotek.com/products/imaging-microscopy-cell-imaging-multi-mode-readers/cytation-5-cell-imaging-multi-mode-reader/) imaging Multi-Mode Reader produced by [Biotek](https://www.biotek.com/).

## About

The Cytation5 reader can store results in an Excel file. This tool reads such an Excel file (all sheets) and extracts the data sets stored. These data sets can the be plotted too (or just used for other analyses)

## Requirements

  - python 3 (tested in 3.7)


## Installation

The installation is straight-forward
### clone repo

```sh
git clone git@github.com:stefanSchinkel/PlateReader.git
```

### setup virtual environment (optional, but recommend)

In order not impact the host system, running everything in a virtual enviroment is recommended.

```sh
# create a new enviroment (needed only once)
python -m -venv .venv
# activate the environment
source .venv/bin/activate
```

### install dependencies

```sh
pip install -r requirements.txt
```

## Usage

### Basic Usage

```sh
python3 PlateReader.py exportfile.xlxs
```

By default, the PlateReader will read all sets in all sheets of the excel file and plot the data with a random (but consistent) colormap for each set and render the plots.

### Advanced Usage
#### ExcelReader

The "heavy lifiting" is done by the the ExcelReader and SetReader class in [
ExcelReader](./lib/ExcelReader.py). ExcelReader will just open an Excel file and pass every sheet to the SetReader and parse the data. The data is stored in ExcelReader.sheets (a dict). Every key in this dict represents on sheet in the Excel file. The sheets in turn contain the data from SetReader (cf below)

#### SetReader

SetReader reads the data from one sheet of the Excelfile and contains multiple entries (one for each marker)



## Limitations

  - currently marker names (in one work sheet) have to be unique
  -


