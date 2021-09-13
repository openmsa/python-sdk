"""Module ConfProfile."""

import json

from msa_sdk.msa_api import MSA_API


class ConfBackup(MSA_API):
    """Class ConfBackup."""

    def __init__(self):
        """
        Initialize.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        MSA_API.__init__(self)
        self.api_path = "/conf-backup"

    def restore(self, device_id: int, revision: str) -> None:
        """
        Restore.

        Parameters
        ----------
        device_id: Integer
                Profile id
        revision: String
                Revision to apply (date or tag name).
                Date format is {"YYYY-MM-DD hh:mm"}

        Returns
        -------
        None
        """
        self.path = "{}/v1/restore/{}/{}".format(self.api_path,
                                                 device_id,
                                                 revision)

        self._call_post()

    def restore_status(self, device_id: int) -> None:
        """
        Restore status.

        Parameters
        ----------
        device_id: Integer
                Profile id

        Returns
        -------
        None
        """
        self.path = "{}/v1/restore-status/{}".format(self.api_path, device_id)

        self._call_put()

    def backup_status(self, device_id: int) -> str:
        """
        Backup Status.

        Parameters
        ----------
        device_id: Integer
                Profile id

        Returns
        -------
        Status: String
        """
        self.path = "{}/v1/backup-status/{}".format(self.api_path, device_id)

        self._call_get()

        return json.loads(self.content)['status']

    def backup(self, device_id: int) -> None:
        """
        Backup Status.

        Parameters
        ----------
        device_id: Integer
                Profile id

        Returns
        -------
        Status: String
        """
        self.path = "{}/v1/backup/{}".format(self.api_path, device_id)

        self._call_post()
