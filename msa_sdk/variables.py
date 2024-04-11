"""Module Variables."""

import json
import os
import sys
import requests

class VariableExistsException(BaseException):
    """Class Exception for variables that already were added."""


class VariableMandatoryException(BaseException):
    """Class Exception for variables that should has value set."""


class Variable:
    """Class Variable."""

    # pylint: disable=too-many-arguments
    def __init__(self, name, var_type='String', values=None, def_values=None,
                 required=False):
        """Init."""
        self._name = name
        self._var_type = var_type
        self._values = values if values else ""
        self._def_values = def_values
        self._required = required

    @property
    def name(self):
        """Property name."""
        return self._name

    @property
    def var_type(self):
        """Property var type."""
        return self._var_type

    @property
    def values(self):
        """Property values."""
        return self._values

    @property
    def default_value(self):
        """Property default value."""
        return self._def_values

    @property
    def required(self):
        """Property required."""
        return self._required

    @property
    def dict(self):
        """Property to convert this object in a dictionary."""
        return {
            'name': self._name,
            'type': self.var_type,
            'values': self.values,
            'default_value': self._def_values
        }


class Variables:
    """Class Variables."""

    def __init__(self):
        """__init__."""
        self.all = []

    # pylint: disable=too-many-arguments
    def add(self, name, var_type='String', values=None, def_value=None,
            required=False) -> None:
        """
        Add a variable.

        Parameters
        ----------
        name: String
            Name of the variable

        var_type: String
            The type of the variable

        values: List
            List of values possible

        def_value: String
            Default value

        required: Bool
            Determine the variable is required

        Returns
        -------
        None


        """
        for var in self.all:
            if var.name == name:
                raise VariableExistsException

        self.all.append(Variable(name, var_type, values, def_value, required))

    def vars_definition(self) -> str:
        """All variables defined.

        Returns
        -------
        json: all variables defined

        """
        variables = []
        for var in self.all:
            variables.append(var.dict)

        return json.dumps(variables)

    @classmethod
    def task_call(cls, var_obj=None):
        """Will print all the variables from an object.

        Parameters
        ----------
        var_obj: Variables
            Variables Object

        Returns
        -------
        Json with all the variables

        """
        if len(sys.argv) > 1 and '--get_vars_definition' in sys.argv[1]:
            if var_obj:
                print(var_obj.vars_definition(), end='')
            else:
                print("[{}]", end='')
            sys.exit(0)
        from msa_sdk import context
        return context

    @classmethod
    def load_context(cls) -> dict:
        """Load context."""
        context = json.loads('{"TOKEN":"12345qwert"}')
        if len(sys.argv) > 2 and '--execute' in sys.argv[1]:
            context = json.loads(open(sys.argv[2]).read())
        elif not os.isatty(0):
            ctx = sys.stdin.read();
            if not ctx:
                return context
            context = json.loads(ctx)

        # Get Auth parameters.

        url = os.environ.get('API_TOKEN_URL') or "http://msa-auth:8080/auth/realms/main/protocol/openid-connect/token"
        params = {"client_id": os.environ["CLIENT_ID"], "grant_type": "client_credentials", "client_secret" : os.environ["CLIENT_SECRET"]}
        response = requests.post(url, data=params)
        data = response.json()
        access_token = data["access_token"]
        #-------------------------------------
        context['TOKEN'] = access_token
        return context


    def check_mandatory_param(self, context) -> None:
        """Check if any required var has no value.

        Parameters
        ----------
        context: Dict
            Context com valores

        Returns
        -------
        None

        """
        for var in self.all:
            if var.required and var.name not in context:
                raise VariableMandatoryException