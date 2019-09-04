"""
Test Repository
"""
from unittest.mock import patch
from urllib.parse import urlencode

from util import repository_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


def test_file_update_comment(repository_fixture):
    """
    Test file update comment
    """

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        repository = repository_fixture
        repository.file_update_comment(
            'Configuration/ABR/ABRA1570/FORTINET/timezone',
            'Comment value')

        data = urlencode({'uri': 'Configuration/ABR/ABRA1570/FORTINET/timezone',
                          'comment': 'Comment value'})

        assert repository.path == '/repository/comment?{}'.format(data)
        mock_call_post.assert_called_once_with()
