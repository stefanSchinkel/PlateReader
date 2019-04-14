#!/usr/bin/env python3

from lib.ExcelReader import ExcelReader

FILE = "/path/to/your/file"

def main():
    # init and read
    er = ExcelReader(FILE)
    er.main()

    # select a sheet
    sheets = list(er.sheets.keys())
    # get all sets
    set_01 = er.sheets[sheets[0]]
    # select one marker from set
    markers = list(set_01.keys())
    # data for marker
    data = set_01[markers[0]]

    # you'll prob want to do sth with it
    return data

if __name__ == '__main__':
    main()
