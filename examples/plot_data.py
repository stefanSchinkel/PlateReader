#!/usr/bin/env python3

from lib.ExcelReader import ExcelReader

FILE = "/path/to/file/"
SHEET = "Plate 2"
MARKER = "miRFP670:637,678"

def main():

    er = ExcelReader(FILE)
    er.main()
    data = er.sheets[SHEET][MARKER]
    data.plot(plot_name=MARKER)

if __name__ == '__main__':
    main()