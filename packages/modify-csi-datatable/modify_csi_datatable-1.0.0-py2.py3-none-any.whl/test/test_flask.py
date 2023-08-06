import os
import modify_csi_datatable
import pytest
import tempfile


class TestCase(object):

    def setUp(self):
        # self.db_fd, modify_csi_datatable.app.config['DATABASE'] = tempfile.mkstemp()
        modify_csi_datatable.app.testing = True
        self.app = modify_csi_datatable.app.test_client()
        # with modify_csi_datatable.app.app_context():
            # modify_csi_datatable.init_db()

    def tearDown(self):
        pass
        # os.close(self.db_fd)
        # os.unlink(modify_csi_datatable.app.config['DATABASE'])


if __name__ == '__main__':
    pytest.main()
