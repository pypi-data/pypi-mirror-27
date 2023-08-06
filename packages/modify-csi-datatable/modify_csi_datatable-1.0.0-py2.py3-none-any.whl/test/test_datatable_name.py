from modify_csi_datatable.modify_csi_datatable import modify_fw_datatable
from modify_csi_datatable.utils import find_string_index, create_proj_fw_chg_log
import pytest
import os
from os import path
import filecmp
import logging
import fileinput

base_dir = os.path.dirname(__file__)
logger = logging.getLogger('test_datatable')
logger.setLevel(logging.DEBUG)

# configure logger
handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
handler_stream = logging.StreamHandler()
handler_stream.setLevel('DEBUG')
handler_stream.setFormatter(handler_stream_formatter)
logger.addHandler(handler_stream)


@pytest.mark.parametrize(("project_fw", "old_tablename", "new_tablename", "validation_project_fw"), [
    ("s3122_pv400_test_das-3.CR300", "fifteenMin", "quinqueMin", "validation_data/s3122_name_test_das-3.CR300")
])
def test_change_datatable_name(tmpdir, project_fw, old_tablename, new_tablename, validation_project_fw):
    print('Testing {}'.format(project_fw))

    # update the date in the change log of the validation file
    validation_file = []
    for line in fileinput.input(validation_project_fw):
        validation_file.append(line.rstrip())

    chg_log_index = find_string_index(validation_file, 'FML: Change Datatable name and interval')
    validation_file[chg_log_index] = create_proj_fw_chg_log('FML')

    with open(validation_project_fw, 'w') as fid:
        fid.write('\n'.join(validation_file))
        fid.write('\n')

    test_dir = tmpdir.mkdir('test_output')

    logger.info('Created tmp directory at {}'.format(test_dir))

    try:
        modify_fw_datatable(
            proj_filepath=project_fw,
            user_initials='FML',
            search_tablename=old_tablename,
            repl_tablename=new_tablename,
            output_dir=test_dir
        )

    except Exception as err:
        logger.debug('{}'.format(err))
        exit(1)

    assert filecmp.cmp(path.join(test_dir, project_fw), validation_project_fw)
