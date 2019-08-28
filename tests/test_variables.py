"""
Test Variables
"""

import json
import sys
import io
from unittest.mock import patch

import pytest

from msa_sdk.variables import Variables
from msa_sdk.variables import Variable
from msa_sdk.variables import VariableExistsException
from msa_sdk.variables import VariableMandatoryException


def test_create_simple_variable():
    """Test Create a Variable."""

    var = Variable('Var1')

    assert var.name == 'Var1'
    assert var.var_type == 'String'
    assert var.values == []
    assert var.default_value is None
    assert not var.required


def test_create_complete_variable():
    """Test create a complete variable with all fields."""

    var = Variable('Var1', var_type='Int', values=[1, 2, 3],
                   def_values='def_value', required=True)

    assert var.name == 'Var1'
    assert var.var_type == 'Int'
    assert var.values == [1, 2, 3]
    assert var.default_value == 'def_value'
    assert var.required


def test_create_vars():
    """
    Test create vars with one object
    """

    variables = Variables()

    variables.add('Var1')

    assert len(variables.all) == 1
    assert variables.all[0].name == 'Var1'
    assert variables.all[0].var_type == 'String'
    assert variables.all[0].values == []
    assert variables.all[0].default_value is None
    assert not variables.all[0].required


def test_create_var_type():
    """
    Test create var with a type
    """

    variables = Variables()

    variables.add('Var2', 'Int')

    assert len(variables.all) == 1
    assert variables.all[0].name == 'Var2'
    assert variables.all[0].var_type == 'Int'
    assert not variables.all[0].required


def test_var_mandatory_fail():
    """
    Test var mandatory
    """

    with pytest.raises(VariableMandatoryException):
        variables = Variables()

        variables.add('Var1')
        variables.add('Var2', required=True)

        context = {'Var1': 'value1'}

        variables.check_mandatory_param(context)


def test_var_mandatory_success():
    """
    Test var mandatory
    """

    variables = Variables()

    variables.add('Var1')
    variables.add('Var2', required=True)

    context = {'Var2': 'value2'}

    variables.check_mandatory_param(context)


def test_create_many_vars():
    """
    Test create many vars
    """

    variables = Variables()

    variables.add('Var1')
    variables.add('Var2', 'Int')
    variables.add('Var3', values=['v1', 'v2'])

    assert len(variables.all) == 3
    assert variables.all[0].name == 'Var1'

    assert variables.all[1].name == 'Var2'
    assert variables.all[1].var_type == 'Int'

    assert variables.all[2].name == 'Var3'
    assert variables.all[2].var_type == 'String'
    assert variables.all[2].values == ['v1', 'v2']


def test_get_definition():
    """
    Test get vars definition
    """

    variables = Variables()

    result_vars = [
        {
            'name': 'Var1',
            'type': 'String',
            'values': [],
            'default_value': None
        },
        {
            'name': 'Var2',
            'type': 'Int',
            'values': [],
            'default_value': None
        },
        {
            'name': 'Var3',
            'type': 'String',
            'values': ['v1', 'v2'],
            'default_value': None
        }
    ]

    variables.add('Var1')
    variables.add('Var2', 'Int')
    variables.add('Var3', values=['v1', 'v2'])

    assert variables.vars_definition() == json.dumps(result_vars)


def test_task_call():
    """
    Test task call to return var definitions
    """

    test_args = ['task.py', '--get_vars_definition']

    with patch.object(sys, 'argv', test_args):
        caputure_output = io.StringIO()
        sys.stdout = caputure_output

        variables = Variables()

        variables.add('Var1')
        variables.add('Var2')
        Variables().task_call(variables)

        sys.stdout = sys.__stdout__
        assert caputure_output.getvalue() == variables.vars_definition()


def test_task_call_wrong_parameter():
    """
    Test task call to return var definitions
    """

    test_args = ['prog', 'task.py', '--something_else']

    with patch.object(sys, 'argv', test_args):
        caputure_output = io.StringIO()
        sys.stdout = caputure_output

        variables = Variables()

        variables.add('Var1')
        variables.add('Var2')
        Variables().task_call(variables)

        sys.stdout = sys.__stdout__
        assert caputure_output.getvalue() == ''


def test_variable_already_defined():
    """
    Test check if variable is defined
    """
    with pytest.raises(VariableExistsException):
        variables = Variables()

        variables.add('Var1')
        variables.add('Var1')
