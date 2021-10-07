import json
from unittest.mock import patch

from util import admin_fixture


def test_get_vars_value(admin_fixture):
    """
    Test if configuration variable value got successfully
    """

    admin = admin_fixture

    test_requested_var_name = 'UBI_VAR_NAME'
    test_response = json.dumps([{
        'name': 'UBI_VAR_NAME',
        'value': 'UBI_VAR_VALUE',
        'comment': ''
    }])
    test_requested_var_value = 'UBI_VAR_VALUE'

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = test_response
        assert admin.get_vars_value(
            test_requested_var_name) == test_requested_var_value
