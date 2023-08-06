#!/usr/bin/env python
from datetime import date
from os import path
import fileinput
import logging


def create_proj_fw_chg_log(initials):
    return "'" + date.today().strftime('%Y-%m-%d') + " " + initials + ': Change Datatable name and interval'


def create_cfg_chg_log(initials):
    return "# " + date.today().strftime('%Y-%m-%d') + " " + initials + ': Change Datatable name and interval'


def find_string_index(sting_list, search_string):
    return [i for i, l in enumerate(sting_list) if search_string in l][0]


def import_file(filepath):
    file_lines = []

    if not path.exists(filepath):
        raise IOError('{} does not exist'.format(filepath))

    if not path.isfile(filepath):
        raise IOError('{} is not a file'.format(filepath))

    for line in fileinput.input(filepath):
        file_lines.append(line.rstrip())

    return file_lines


def setupLogger(name, loglevel, logfilename):
    logger = logging.getLogger(name)

    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # configure logger
    logger.setLevel(logging.DEBUG)
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(handler_stream_formatter)
    handler_stream.setLevel(loglevel.upper())
    logger.addHandler(handler_stream)

    if logfilename != '':
        handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        logger.debug('Log Filename is: %s' % handler_file)
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        # handler_file.setLevel(level.DEBUG)
        logger.addHandler(handler_file)

    logger.debug('Log Level is: %s' % loglevel)
    logger.debug('Log Filename is: %s' % logfilename)

    return logger
