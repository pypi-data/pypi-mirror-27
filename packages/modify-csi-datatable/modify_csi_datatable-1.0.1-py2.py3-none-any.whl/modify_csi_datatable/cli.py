#!/usr/bin/env python
import fileinput
import logging
import re
from operator import itemgetter
from os import path
from sys import exit

from .modify_csi_datatable import ModifyCsiDatatable

if __name__ == "__main__":
    from argparse import ArgumentParser
    arg_parser = ArgumentParser(description='Utility to change a data table name and interval')
    arg_parser.add_argument('proj_cfg_file', help='path of the project config file', metavar='PATH')
    arg_parser.add_argument('proj_fw_file', help='path of the project firmware file', metavar='PATH')
    arg_parser.add_argument('dt_name_new', help='the name to change the data table to')
    arg_parser.add_argument('dt_interval_new', help='path of the project firmware file')
    arg_parser.add_argument('-n', '--name', default='fifteenMin', help='the name of the data table to change')
    arg_parser.add_argument('-i', '--interval', default=15, help='the data table interval to change')
    arg_parser.add_argument('-p', '--path', help='the folder to look for the project files in')
