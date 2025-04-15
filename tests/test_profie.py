"""
Test Profile
"""

from unittest.mock import patch

from util import profile_fixture


def test_exist(profile_fixture):
    """
    Test exist profile by reference
    """
    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        profile = profile_fixture
        reference = "test1"
        profile.exist(reference)

        assert profile.path == "/profile/v1/exist/test1"
        mock_call_post.assert_called_once()