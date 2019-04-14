#!/usr/bin/env python3

#path hack to make examples run-able
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from lib.ExcelReader import ExcelReader

FILE = "/path/to/your/file"
SHEET = "Plate 2"
MARKER = "mCherry:583,616"

def main():

    er = ExcelReader(FILE)
    er.main()
    data = er.sheets[SHEET][MARKER]
    data.plot(plot_name=MARKER)

if __name__ == '__main__':
    main()