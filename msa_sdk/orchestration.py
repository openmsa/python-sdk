"""Module Orchestration."""

import json
import time

from msa_sdk import constants
from msa_sdk.msa_api import MSA_API
from msa_sdk.variables import Variables


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
        self._call_get()

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

        self._call_get()

    def read_service_instance_by_condition(self, services_to_search: list, service_instance_id: int, service_external_reference: str, process_instance_id: int, service_execution_status: str, service_variables: list):
        """
        Read service instance by condition.

        Parameters
        ----------
        services_to_search: list
        ["str","str"]
        service_instance_id: int
        service_external_reference: string
        process_instance_id: int
        service_execution_status: string
        service_variables: list
        [
            {
            "variable": "apps_to_deploy[0].app_port",
            "operator": "=",
            "value": "80",
            "next_condition_joinOperator": "OR"
            },
            {
            "variable": "deployment_name",
            "operator": "=",
            "value": "Wordpress",
            "next_condition_joinOperator": ""
            }
        ]
        Returns
        -------
        serviceIds

        """

        data = {
            "servicesToSearch" : services_to_search,
            "serviceInstanceId" : service_instance_id,
            "serviceExternalReference" : service_external_reference,
            "processInstanceId": process_instance_id,
            "serviceExecutionStatus": service_execution_status,
            "serviceVariables" : service_variables
        }
        self.path = "{}/search/{}/service/instance".format(self.api_path,
                                                           self.ubiqube_id)
        self.call_post(data)
        return self.content

    
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

        self._call_get()

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

        self._call_get()

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

        self._call_post()

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

        self._call_delete()

    def execute_service(self, service_name: str, process_name: str,
                        data: dict):
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

        self._call_post(data)

        service_id = None
        try:
            service_id = int(json.loads(self.content)['serviceId']['id'])
        except BaseException:
            pass

        return service_id

    def execute_service_process(self, service_name: str, process_name: str,
                                data: dict):
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
        Tuple
        process_id: Integer
                    Id if execution was success, -1 if execution fails

        service_id: Integer
                    Id if execution was success, -1 if execution fails

        """
        format_path = ('/orchestration/service/execute/{}'
                       '?serviceName={}&processName={}&serviceInstance=0')

        self.path = format_path.format(self.ubiqube_id,
                                       service_name, process_name)

        self._call_post(data)

        try:
            service_id = int(json.loads(self.content)['serviceId']['id'])
        except KeyError:
            service_id = -1

        try:
            process_id = int(json.loads(self.content)['processId']['id'])
        except KeyError:
            process_id = -1

        return service_id, process_id

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

        self._call_post(data)

    def execute_service_by_reference(self, external_ref, service_ref,
                                     service_name, process_name, data, timeout = 180, interval = 5):
        """

        Execute service (start it, don't wait the end). If the instance is already running, it will wait the end of the current before to run this instance to prevent error.

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


        running = True
        global_timeout  = time.time() + timeout
        while (running and time.time() <= global_timeout) :
          try:
            self.path = format_path.format(external_ref, service_ref, service_name, process_name)
            self._call_post(data)
            running = False
          except TypeError as e:   
            #Got type error when the process is already running
            dev_var              = Variables()
            context              = Variables.task_call(dev_var)
            if context.get('PROCESSINSTANCEID'):
              self.update_asynchronous_task_details(context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'], 'Waiting end of previous excecution for WF  '+service_name.rsplit('/', 1)[1]+' with instance ref '+str(service_ref))
            time.sleep(interval)  
          
        if running:
            dev_var              = Variables()
            context              = Variables.task_call(dev_var)
            MSA_API.task_error('Timeout for waiting end of previous excecution WF  '+service_name.rsplit('/', 1)[1]+', it still running with instance ref '+str(service_ref)+ ' for execute_service_by_reference', context, True) 

        
    def wait_and_run_execute_service_by_reference(self, ubiqube_id, service_external_ref, service_name, process_name, data, timeout = 300, interval = 10):
        """

        For the given instance reference, if the instance is already running, it will wait the end of the current execution and after execute the instance (cf execute_service_by_reference) and wait the end of this new execution and return the response (to get the status, used response['status']['status'] and to get the details : response['status']['details'] ). Timeout for previous instance and timeout for new instance.

        Parameters
        ----------
        ubiqube_id: String
                ubiqube_id                  like "NTTA14"
        service_external_ref: String
                Service external reference  like "NTTSID2867"
        service_name: String
                Service name  like "Process/workflows/test_wait_and_run_execute_service_by_reference/test_wait_and_run_execute_service_by_reference"
        process_name: String
                Process name like "Process/workflows/test_wait_and_run_execute_service_by_reference/Process_very_long_task"
        data: Json
                data json    like dict(playbook='pb1')
        timeout: Integer
                Timeout
        interval: Integer
                interval

        Returns
        -------
        response

        """
        dev_var              = Variables()
        context              = Variables.task_call(dev_var)
     
        global_timeout       = time.time() + timeout
        service_instance_id  = int(service_external_ref[6:])
        status               = None
       
        self.execute_service_by_reference(ubiqube_id, service_external_ref, service_name, process_name, data, timeout, interval)
         
        #Wait the end of the new run :
        if service_instance_id and isinstance(service_instance_id, int) :
          while time.time() <= global_timeout:
            status = self.get_service_status_by_id(service_instance_id)
            if status != constants.RUNNING  :
                break
            if context.get('PROCESSINSTANCEID'):
              self.update_asynchronous_task_details(context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'], 'Running WF  '+service_name.rsplit('/', 1)[1]+', for instance ref '+str(service_external_ref))
            time.sleep(interval)
        
        if time.time() >= global_timeout:
          MSA_API.task_error('Timeout, WF  '+service_name.rsplit('/', 1)[1]+' is still running with instance ref '+str(service_external_ref), context, True) 
        
        response = json.loads(self.content)
        if isinstance(response, list):
          return response[0]
        else:
          #for automatic test
          return response    



    def wait_end_get_process_instance(self, process_id, timeout = 600, interval=5):
        """

        Wait that wf instance has finish and return the final dict result (where the status value is ENDED or FAILED).

        Parameters
        ----------
        process_id: Integer
                Process ID
        timeout: Integer
                Timeout
        interval: Integer
                interval
        Returns
        -------
        response

        """
        response = {}
        global_timeout = time.time() + timeout
        while time.time() < global_timeout:
            #get service instance execution status.
            self.get_process_instance(process_id)
            response = json.loads(self.content)
            status = response.get('status').get('status')
            if status != constants.RUNNING:
                break
            time.sleep(interval)

        return response
 

    def resume_failed_or_paused_process_instance(self, process_id):
        """

        Resume a FAILED or PAUSED process instance.

        Parameters
        ----------
        process_id: Integer

        Returns
        -------
        None

        """
        format_path = ('/orchestration/v2/process/{}/resume')

        self.path = format_path.format(process_id)

        self._call_post()
        
    def execute_launch_process_instance(self, service_id, process_name, data):
        """

        Execute launch process service.

        Parameters
        ----------
        service_id: Integer
                Service ID
        process_name: String
                Process name
        data:         dict()
                      A dictionary containing workflow variables

        Returns
        -------
        None

        """
        format_path = ('/orchestration/process/execute/{}/{}?processName={}')

        self.path = format_path.format(self.ubiqube_id,
                                       service_id, process_name)

        self._call_post(data)

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

        self._call_get()

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
        self._call_get()

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
        self._call_put(data)

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
        self._call_put()

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
        self.path = '{}/services?ubiqubeId={}&range={}'.format(
            self.api_path_v1, self.ubiqube_id, range)
        self._call_get()

        return json.loads(self.content)

    def get_service_status_by_id(self, service_id: int):
        """

        Return service status by service_id.

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
        self.path = '{}/service/process-instance/{}'.format(
            self.api_path_v1, service_id)
        self._call_get()

        try:
            status = json.loads(self.content)[0]['status']['status']
        except BaseException:
            status = None

        return status

    def get_process_status_by_id(self, process_id: int):
        """

        Return process status by process_id.

        Parameters
        ----------
        process_id: Integer
                    Id of workflow instance

        Returns
        -------
        String: RUNNING|FAIL|ENDED
                Status of the service
        OR
        None:   In case if execution failed

        """
        self.path = '{}/process-instance/{}'.format(
            self.api_path_v1, process_id)
        self._call_get()

        try:
            status = json.loads(self.content)['status']['status']
        except BaseException:
            status = None

        return status

    def attach_wf_to_subtenant(self, ubiqubeIds, uri):
        """
        
        Attach workflows to subtenants : POST /orchestration/service/attach.

        Parameters
        ----------
        uri: String
              uri corresponds to the relative path of the XML file of the repository. The relative path starts from Process and includes the .xml at the end. Example = Process/workflows/AutoAttached/organizations.xml
        ubiqubeIds: String
                ubiqubeIds corresponds to the customer ids including the prefix. Example UBIA234

        Returns
        -------
        None

        """
        self.path = "{}/service/attach?ubiqubeIds={}&uri={}".format(self.api_path, ubiqubeIds, uri)
        self._call_post()
