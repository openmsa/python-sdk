"""
Test Geolocation
"""
from unittest.mock import patch

from msa_sdk.geolocation import Geolocation


def test_geolocation():

    me_id = 125
    latitude = 45.150121
    longitude = 5.725408

    geoloc = Geolocation(me_id)

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        geoloc.set_geolocation(latitude, longitude)
        mock_call_put.assert_called_once()

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        geo_loc = geoloc.get_geolocation()
        mock_call_get.assert_called_once()
