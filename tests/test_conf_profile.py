"""
Test Repository
"""
import json
from unittest.mock import patch
from urllib.parse import urlencode

from util import conf_profile_fixture


def test_create(conf_profile_fixture):
    """
    Test create configuration profile
    """

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        conf_profile = conf_profile_fixture
        conf_profile.customer_id = 10
        conf_profile.create()

        assert conf_profile.path == "/conf-profile/v2/10"
        mock_call_post.assert_called_once()


def test_read(conf_profile_fixture):
    """
    Test get configuration profile.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_get') as mock_call_get:
        conf_profile = conf_profile_fixture
        conf_profile.profile_id = 200
        conf_profile.read()
        
        assert conf_profile.path == "/conf-profile/v2/200"
        mock_call_get.assert_called_once_with()



def test_update(conf_profile_fixture):
    """
    Test update configuration profile.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        params = json.dumps({
                    "name": "Updated Name",
                    "externalReference": "htoPR148",
                    "comment": "This is Comment",
                    "model": {
                        "id": 14020601
                    },
                    "vendor": {
                        "id": 14020601
                    },
                    "microserviceUris": [
                        "CommandDefinition/LINUX/SYSTEM/user.xml"
                    ],
                    "templateUris": [],
                    "attachedManagedEntities": [
                        202
                    ]
                })
        name = "Updated Name"
        conf_profile = conf_profile_fixture
        conf_profile.name = name
        conf_profile.update()
        
        assert conf_profile.path == "/conf-profile/v2/148?customer_id=9"
        assert conf_profile.name == name
        mock_call_put.assert_called_once_with(params)


def test_delete(conf_profile_fixture):
    """
    Test delete configuration profile.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_delete') as mock_call_delete:
        conf_profile = conf_profile_fixture
        conf_profile.delete()
        
        assert conf_profile.path == "/conf-profile/v2/148"
        mock_call_delete.assert_called_once_with()
