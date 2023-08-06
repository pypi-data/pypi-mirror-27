#!/usr/bin/env python
import logging
import re
from os import path, getcwd
from sys import exit, version_info

if version_info.major == 2:
    from utils import create_proj_fw_chg_log, find_string_index, import_file
elif version_info.major == 3 and version_info.minor == 5:
    from utils import create_proj_fw_chg_log, find_string_index, import_file
elif version_info.major == 3 and version_info.minor == 6:
    from utils import create_proj_fw_chg_log, find_string_index, import_file


def modify_fw_datatable(
        proj_filepath, user_initials, search_tablename='fifteenMin',
        repl_tablename='', interval=15, units='MIN', output_dir=''
):
    logger = logging.getLogger('modify_csi_datatable')
    logger.setLevel(logging.DEBUG)

    try:
        code = import_file(proj_filepath)

        # insert the change log
        chg_log_start_index = find_string_index(code, '## Change Log')
        code.insert(chg_log_start_index + 1, create_proj_fw_chg_log(user_initials))

        if units.lower() not in ["msec", "sec", "min", "hr", "day", "mon"]:
            raise ValueError(
                '"{}" is not a valid CSI data interval.  Valid units are msec, sec, min, hr, day, mon'.format(units)
            )

        # find the start of the data table
        try:
            tb_start_index = find_string_index(code, 'DataTable(' + search_tablename)
        except Exception as err:
            logger.debug(err)
            tb_start_index = find_string_index(code, 'DataTable(' + repl_tablename)

        tb_end_index = [i for i, l in enumerate(list(code)) if 'EndTable' in l and i > tb_start_index][0]

        logger.debug('Found DataTable start at line {}'.format(tb_start_index))
        logger.debug('Found DataTable end at line {}'.format(tb_end_index))

        for i, l in enumerate(list(code)):
            if tb_start_index <= i <= tb_end_index and 'DataInterval' in l:
                # Draker specifies the data table interval in all CAPS, but CSI is case in-sensitive
                # Updating the line: DataInterval(0, 15, MIN, 0)
                logger.debug('Found the DataInterval line: {}'.format(l))
                code[i] = re.sub(r'\bMIN,\b', units.upper(), l)
                code[i] = re.sub(r',\s*\d+,', ', {},'.format(interval), l)
                logger.debug('New DataInterval line: {}'.format(l))

            elif search_tablename in l:
                logger.debug('Found the DataTable Name in line: {}'.format(i))
                code[i] = l.replace(search_tablename, repl_tablename)
                logger.debug('Updated line: {}'.format(code[i]))

        if output_dir is not '':
            proj_filepath = path.join(output_dir, path.basename(proj_filepath))

        with open(proj_filepath, 'w') as fid:
            fid.write('\n'.join(code))
            fid.write('\n')

    except IOError as err:
        logger.error(err)
        exit(1)


if __name__ == "__main__":
    from argparse import ArgumentParser

    module_logger = logging.getLogger('modify_csi_datatable')
    module_logger.setLevel(logging.DEBUG)

    # configure logger
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setLevel('DEBUG')
    handler_stream.setFormatter(handler_stream_formatter)
    module_logger.addHandler(handler_stream)

    arg_parser = ArgumentParser(description='Utility to change a data table name')
    arg_parser.add_argument('user_initials', help='initials of the user executing the change')
    arg_parser.add_argument('proj_fw_file', help='path of the project firmware file', metavar='PATH')
    arg_parser.add_argument('dt_name_new', default='quinqueMin', help='the name to change the data table to')
    arg_parser.add_argument('dt_interval_new', default=5, help='path of the project firmware file')
    arg_parser.add_argument('-n', '--name', default='fifteenMin', help='the name of the data table to change')
    arg_parser.add_argument('-p', '--path', default='', help='the folder to look for the project files in')

    args = arg_parser.parse_args()
    cwd = path.normcase(getcwd())

    # create temporary directory if the project file path is not specified
    if args.path is '':
        args.path = getcwd()
    else:
        args.path = path.normcase(path.normpath(args.path))

    try:
        modify_fw_datatable(
            proj_filepath=path.join(args.path, args.proj_fw_file),
            user_initials=args.user_initials,
            search_tablename=args.name,
            repl_tablename=args.dt_name_new,
            interval=args.dt_interval_new,
            output_dir=args.path
        )

    except IOError as err:
        module_logger.debug('{}'.format(err))
        exit(1)

    except Exception as err:
        module_logger.debug('{}'.format(err))
        exit(1)


