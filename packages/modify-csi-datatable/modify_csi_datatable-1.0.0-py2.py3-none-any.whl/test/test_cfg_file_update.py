from modify_csi_datatable.modify_cfg_file import modify_cfg_file
from modify_csi_datatable.utils import find_string_index, create_cfg_chg_log
import pytest
import os
from os import path
import filecmp
import fileinput
import logging

base_dir = os.path.dirname(__file__)
logger = logging.getLogger('test_cfg_file_update')
logger.setLevel(logging.DEBUG)

# configure logger
handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
handler_stream = logging.StreamHandler()
handler_stream.setLevel('DEBUG')
handler_stream.setFormatter(handler_stream_formatter)
logger.addHandler(handler_stream)


@pytest.mark.parametrize(("cfg_file", "old_tablename", "new_tablename", "interval", "units", "validation_cfg_file"), [
    (
            "s3122_pv400_test_das-3.cfg",
            "fifteenMin",
            "quinqueMin",
            5,
            "MIN",
            "validation_data/s3122_name_test_das-3.cfg"
    ),
    (
            "s3122_pv400_test_das-3.cfg",
            "fifteenMin",
            "",
            5,
            "MIN",
            "validation_data/s3122_interval_test_das-3.cfg"
    ),
])
def test_change_datatable_interval(tmpdir, cfg_file, old_tablename, new_tablename, interval, units, validation_cfg_file):
    logger.info('Testing {}'.format(cfg_file))

    cfg_filepath = path.join(base_dir, path.normpath(cfg_file))

    # update the date in the change log of the validation file
    validation_file = []
    for line in fileinput.input(validation_cfg_file):
        validation_file.append(line.rstrip())

    chg_log_index = find_string_index(validation_file, 'FML: Change Datatable name and interval')
    validation_file[chg_log_index] = create_cfg_chg_log('FML')

    with open(validation_cfg_file, 'w') as fid:
        fid.write('\n'.join(validation_file))
        fid.write('\n')

    # create a temporary testing directory
    test_dir = tmpdir.mkdir('test_output')

    logger.info('Created tmp directory at {}'.format(test_dir))

    try:
        modify_cfg_file(
            cfg_filepath, 'FML', repl_tablename=new_tablename, interval=interval, units=units, output_dir=test_dir
        )

    except Exception as err:
        logger.debug('{}'.format(err))
        exit(1)

    test_output_dir = path.join(test_dir, cfg_file)
    logger.debug('{}'.format(test_output_dir))
    assert filecmp.cmp(test_output_dir, validation_cfg_file)
