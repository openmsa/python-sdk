"""
Test Repository
"""
from unittest.mock import MagicMock
from unittest.mock import patch

from util import conf_backup_fixture


def test_restore(conf_backup_fixture):
    """
    Test restore
    """

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        conf_backup = conf_backup_fixture

        conf_backup.restore(200, "2021-09-22 10:21")

        assert conf_backup.path == \
            "/conf-backup/v1/restore/200/2021-09-22 10:21"
        mock_call_post.assert_called_once_with()


def test_restore_status(conf_backup_fixture):
    """
    Tetst restore status
    """

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        conf_backup = conf_backup_fixture

        conf_backup.restore_status(200)

        assert conf_backup.path == \
            "/conf-backup/v1/restore-status/200"
        mock_call_put.assert_called_once_with()


def test_backup_status(conf_backup_fixture):
    """Test Backup Status"""

    with patch('requests.get') as mock_get:
        conf_backup = conf_backup_fixture

        mock_get.return_value.text = ('{"message": "Backup successful",'
                                      ' "status": "RUNNING"}')

        conf_backup.backup_status(200)

        assert conf_backup.path == \
            "/conf-backup/v1/backup-status/200"


def test_backup_status_content(conf_backup_fixture):
    """Test Backup Status content"""

    with patch('requests.get') as mock_get:
        conf_backup = conf_backup_fixture

        mock_get.return_value.text = ('{"message": "Backup successful",'
                                      ' "status": "RUNNING"}')

        assert conf_backup.backup_status(200) == "RUNNING"


def test_backup(conf_backup_fixture):
    """Test backup"""

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        conf_backup = conf_backup_fixture

        conf_backup.backup(200)

        assert conf_backup.path == "/conf-backup/v1/backup/200"
        mock_call_post.assert_called_once_with()
