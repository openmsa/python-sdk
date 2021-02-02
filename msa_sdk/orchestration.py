"""Module Orchestration."""

import json

from msa_sdk.msa_api import MSA_API


class Orchestration(MSA_API):
    """Class Orchestration."""

    def __init__(self, ubiqube_id):
        """Initialize."""
        MSA_API.__init__(self)
        self.api_path_v1 = "/orchestration/v1"
        self.api_path = "/orchestration"
        self.ubiqube_id = ubiqube_id

    def list_service_instances(self):
        """
        List service instances.

        Returns
        -------
        None

        """
        self.action = 'List service instances'
        self.path = "{}/{}/service/instance".format(self.api_path,
                                                    self.ubiqube_id)
        self.call_get()

    def read_service_instance(self, service_id):
        """
        Read service instance.

        Parameters
        ----------
        service_id: Integer
                Service ID

        Returns
        -------
        None

        """
        self.action = 'Read service instances'
        self.path = "{}/{}/service/instance/{}".format(self.api_path,
                                                       self.ubiqube_id,
                                                       service_id)

        self.call_get()

    def get_service_variables(self, service_id):
        """

        Get service variables.

        Parameters
        ----------
        service_id: Integer
                Service ID

        Returns
        -------
        None

        """
        self.path = "{}/service/variables/{}".format(self.api_path,
                                                     service_id)

        self.call_get()

    def get_service_variable_by_name(self, service_id, variable_name):
        """
        Get services variable by name.

        Parameters
        ----------
        service_id: Integer
                Service ID
        variabel_name: String
                Name of the variable

        Returns
        -------
        None

        """
        self.path = "{}/service/variables/{}/{}".format(self.api_path,
                                                        service_id,
                                                        variable_name)

        self.call_get()

    def update_service_variable(self, service_id, variable_name, new_value):
        """
        Update service variable.

        Parameters
        ----------
        service_id: Integer
                Service ID
        variabel_name: String
                Name of the variable
        new_value: String
                New servie variable name

        Returns
        -------
        None

        """
        self.path = "{}/service/variables/{}/{}?value={}".format(self.api_path,
                                                                 service_id,
                                                                 variable_name,
                                                                 new_value)

        self.call_post()

    def delete_service(self, service_id):
        """

        Delete service.

        Parameters
        ----------
        service_id: Integer
                Service ID

        Returns
        -------
        None

        """
        self.path = \
            '/orchestration/{}/service/instance/{}'.format(self.ubiqube_id,
                                                           service_id)

        self.call_delete()

    def execute_service(self, service_name: str, process_name: str, data) -> None:
        """

        Execute service.

        Parameters
        ----------
        service_name: String
                      Service Name
        process_name: String
                      Process name
        data:         dict()
                      A dictionary containing workflow variables

        Returns
        -------
        None
             If the execution was failed
        service_id: Integer
                    If execution was success

        """
        format_path = ('/orchestration/service/execute/{}'
                       '?serviceName={}&processName={}&serviceInstance=0')

        self.path = format_path.format(self.ubiqube_id,
                                       service_name, process_name)

        self.call_post(data)

        try:
            service_id = int(json.loads(self.content)['serviceId']['id'])
        except:
            service_id = None

        return service_id        

    # pylint: disable=too-many-arguments
    def execute_by_service(self, external_ref, service_ref, service_name,
                           process_name, data):
        """

        Execute by service.

        Parameters
        ----------
        external_ref: String
                External reference
        service_ref: String
                service reference
        service_name: String
                service name
        process_name: String
                Process name
        data: Json
                data json

        Returns
        -------
        None

        """
        format_path = ('/orchestration/service/execute/{}/{}'
                       '?serviceName={}&processName={}')

        self.path = format_path.format(external_ref, service_ref,
                                       service_name, process_name)

        self.call_post(data)

    def execute_service_by_reference(self, external_ref, service_ref,
                                     service_name, process_name, data):
        """

        Execute service.

        Parameters
        ----------
        external_ref: String
                external reference
        service_reference: String
                Service reference
        service_name: String
                Service name
        process_name: String
                Process name
        data: Json
                data json

        Returns
        -------
        None

        """
        format_path = ('/orchestration/service/execute/{}/{}'
                       '?serviceName={}&processName={}')

        self.path = format_path.format(external_ref, service_ref, service_name,
                                       process_name)

        self.call_post(data)

    def execute_launch_process_instance(self, service_id, process_name, data):
        """

        Execute launch process service.

        Parameters
        ----------
        service_id: Integer
                Service ID
        process_name: String
                Process name

        Returns
        -------
        None

        """
        format_path = ('/orchestration/process/execute/{}/{}?processName={}')

        self.path = format_path.format(self.ubiqube_id,
                                       service_id, process_name)

        self.call_post(data)

    def list_process_instances_by_service(self, service_id):
        """

        List process instances by Service.

        Parameters
        ----------
        service_id: Integer
                Service ID

        Returns
        -------
        None

        """
        self.path = '{}/process/instances/{}'.format(self.api_path,
                                                     service_id)

        self.call_get()

    def get_process_instance(self, service_id):
        """

        Get process instance.

        Parameters
        ----------
        service_id: Integer
                Service ID

        Returns
        -------
        None

        """
        self.path = '{}/process/instance/{}'.format(self.api_path,
                                                    service_id)
        self.call_get()

    def update_process_script_details(self, process_id, task_id, exec_number,
                                      data=None):
        """

        Update process script details.

        Parameters
        ----------
        process_id: Integer
                Process ID
        task_id: Integer
                Task ID
        exec_number: Integer
                Number exec

        Returns
        -------
        None

        """
        self.path = ('{}/process/instance/{}/task/{}'
                     '/execnumber/{}/update').format(self.api_path,
                                                     process_id, task_id,
                                                     exec_number)
        self.call_put(data)

    def update_service_instance_reference(self, service_id, service_ref):
        """

        Update service instance reference.

        Parameters
        ----------
        service_id: Integer
                Process ID
        service_ref: Integer
                Service reference

        Returns
        -------
        None

        """
        self.path = ('{}/{}/service/instance/update/{}'
                     '/?serviceReference={}').format(self.api_path,
                                                     self.ubiqube_id,
                                                     service_id, service_ref)
        self.call_put()

    def update_asynchronous_task_details(self, process_id: int, task_id: int,
                                         exec_number: int,
                                         data: str) -> None:
        """

        Update task comments in GUI dynamically.

        Parameters
        ----------
        process_id: Integer
                Process ID
        task_id: Integer
                Task ID
        exec_number: Integer
                Number exec
        data: String
              Task comment

        Returns
        -------
        None

        """
        details_json = json.dumps({'details': data})
        self.update_process_script_details(
            process_id, task_id, exec_number, details_json)

    def get_list_service_by_status(self, range: int) -> dict:
        """

        List services by status.

        Parameters
        ----------
        range: Integer
               Number of days for the statistic

        Returns
        -------
        Dict()
              Key:   Name of service
              Value: Statistics by status

        """
        self.path = '{}/services?ubiqubeId={}&range={}'.format(self.api_path_v1, self.ubiqube_id, range)
        self.call_get()

        return json.loads(self.content)   


    def get_service_status_by_id(self, service_id: int) -> str:
        """

        Return service status by service_id

        Parameters
        ----------
        service_id: Integer
                    Id of workflow instance

        Returns
        -------
        String: RUNNING|FAIL|ENDED
                Status of the service
        OR
        None:   In case if execution failed

        """
        self.path = '{}/service/process-instance/{}'.format(self.api_path_v1, service_id)
        self.call_get()

        try:
            status = json.loads(self.content)[0]['status']['status']
        except:
            status = None

        return status
