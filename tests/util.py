"""Module test util."""
import json
import pytest

from sdk.device import Device


def _is_valid_json(msg_json):
    try:
        json.loads(msg_json)
    except ValueError:
        return False
    return True


@pytest.fixture
def device_fixture():
    """Device fixture."""
    device = Device(10, "MyDevice", 11, 13, "ncroot", "pswd",
                    "adm_pswd", "mng_addres", "Dexternal", device_id=1234)
    return device
