import json
from unittest.mock import patch

from util import pops_fixture


def test_save_pops_saves_data_correctly(pops_fixture):
    pops = pops_fixture
    test_data = {"key": "value"}

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        mock_call_post.return_value.status_code = 200
        pops.save_pops(test_data)
        assert pops.path == '/sase/pops'
        mock_call_post.assert_called_once_with(test_data)


def test_remove_pop_removes_correct_pop(pops_fixture):
    pops = pops_fixture
    entity_type = "type1"
    vendor = "vendor1"
    name = "pop1"

    with patch('requests.delete') as mock_call_delete:
        mock_call_delete.return_value.status_code = 200
        pops.remove_pop(entity_type, vendor, name)
        assert pops.path == '/sase/pops?entityType={}&vendor={}&name={}'.format(entity_type, vendor, name)
        mock_call_delete.assert_called_once()


def test_save_tunnel_saves_tunnel_data(pops_fixture):
    pops = pops_fixture
    test_data = {"tunnel": "data"}

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        mock_call_post.return_value.status_code = 200
        pops.save_tunnel(test_data)
        assert pops.path == '/sase/pops/tunnel'
        mock_call_post.assert_called_once_with(test_data)


def test_update_tunnel_updates_correct_tunnel(pops_fixture):
    pops = pops_fixture
    cpe_device_id = 123
    pop_vendor = "vendor1"
    pop_identifier = "identifier1"
    test_data = {"update": "data"}

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        mock_call_put.return_value.status_code = 200
        pops.update_tunnel(cpe_device_id, pop_vendor, pop_identifier, test_data)
        assert pops.path == '/sase/pops/tunnel?cpeDeviceId={}&popVendor={}&popIdentifier={}'.format(cpe_device_id,
                                                                                                    pop_vendor,
                                                                                                    pop_identifier)
        mock_call_put.assert_called_once_with(json.dumps(test_data))


def test_list_tunnels_returns_tunnels(pops_fixture):
    pops = pops_fixture
    tenant_prefix = "tenant1"
    location_id = 456
    test_response = {"tunnels": []}

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        mock_call_get.return_value = test_response
        result = pops.list_tunnels(tenant_prefix, location_id)
        assert pops.path == '/sase/pops/tunnels?tenantPrefix={}&locationId={}'.format( tenant_prefix, location_id)
        assert result == test_response
        mock_call_get.assert_called_once()


def test_remove_tunnel_removes_correct_tunnel(pops_fixture):
    pops = pops_fixture
    cpe_device_id = 123
    pop_vendor = "vendor1"
    pop_identifier = "identifier1"

    with patch('requests.delete') as mock_call_delete:
        mock_call_delete.return_value.status_code = 200
        pops.remove_tunnel(cpe_device_id, pop_vendor, pop_identifier)
        assert pops.path == '/sase/pops/tunnel?cpeDeviceId={}&popVendor={}&popIdentifier={}'.format(cpe_device_id,
                                                                                                    pop_vendor,
                                                                                                    pop_identifier)
        mock_call_delete.assert_called_once()
