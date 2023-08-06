#!/usr/bin/env python
import fileinput
import logging
import re
from operator import itemgetter
from os import path
from sys import exit, version_info

if version_info.major == 2:
    from utils import create_cfg_chg_log, find_string_index, import_file
elif version_info.major == 3 and version_info.minor == 5:
    from utils import create_cfg_chg_log, find_string_index, import_file
elif version_info.major == 3 and version_info.minor == 6:
    from utils import create_cfg_chg_log, find_string_index, import_file


def modify_cfg_file(
        cfg_filepath, user_initials, search_tablename='fifteenMin',
        repl_tablename='', interval=15, units='MIN', output_dir=''
):
    logger = logging.getLogger('modify_cfg_file')
    logger.setLevel(logging.DEBUG)

    try:
        cfg_file = import_file(cfg_filepath)

        chg_log_start_index = find_string_index(cfg_file, '# Change Log')
        cfg_file.insert(chg_log_start_index + 1, create_cfg_chg_log(user_initials))

        # find end of change log
        for i, l in enumerate(cfg_file):
            if i > chg_log_start_index:
                if re.match(r'# [0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [a-zA-Z]{2,3}', cfg_file[i - 1]) and l is "":
                    if repl_tablename is not '':
                        cfg_file.insert(i + 1, '# DATA TABLE: RENAME ' + search_tablename + ' ' + repl_tablename)
                        cfg_file.insert(
                            i + 2,
                            '# DATA TABLE: INTERVAL ' + repl_tablename + ' ' + str(interval) + ' ' + units
                        )
                        cfg_file.insert(i + 3, '')
                    else:
                        cfg_file.insert(
                            i + 1,
                            '# DATA TABLE: INTERVAL ' + search_tablename + ' ' + str(interval) + ' ' + units
                        )
                        cfg_file.insert(i + 2, '')

        if output_dir is not '':
            cfg_filepath = path.join(output_dir, path.basename(cfg_filepath))

        with open(cfg_filepath, 'w') as fid:
            fid.write('\n'.join(cfg_file))
            fid.write('\n')

    except IOError as err:
        logger.error(err)
        exit(1)


if __name__ == "__main__":
    from argparse import ArgumentParser
    arg_parser = ArgumentParser(description='Utility to change a data table name and interval')
    arg_parser.add_argument('proj_cfg_file', help='path of the project config file', metavar='PATH')
    arg_parser.add_argument('dt_name_new', help='the name to change the data table to')
    arg_parser.add_argument('dt_interval_new', help='path of the project firmware file')
    arg_parser.add_argument('-n', '--name', default='fifteenMin', help='the name of the data table to change')
    arg_parser.add_argument('-i', '--interval', default=15, help='the data table interval to change')
    arg_parser.add_argument('-p', '--path', help='the folder to look for the project files in')
