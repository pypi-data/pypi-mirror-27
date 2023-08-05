import logging
from datetime import datetime

import requests

from file import File_Backup
from service import Service


class ES_Backup(File_Backup, Service):
    """
    Elasticsearch Backup class
    """

    def __init__(self, hostname=None, backup_name=None):
        self.log = logging.getLogger('backup.elastic')
        if hostname and backup_name:
            self.log.debug("Setting Hostname: {}; Backup: {}".format(hostname, backup_name))
            self.hostname = hostname
            self.backup_name = backup_name
        else:
            msg = "Either the hostname or backup_name is missing. \n hostname:{} \n backup_name:{}".format(
                self.hostname, self.backup_name)
            self.log.error(msg)
            raise ValueError(msg)

    @property
    def hostname(self):
        """
        Hostname of the ES Cluster
        """
        return self._hostname

    @hostname.setter
    def username(self, arg):
        """
        Setter for hostname
        """
        self._hostname = arg

    @property
    def backup_name(self):
        """
        Name of the backup repository in ES
        """
        return self._backup_name

    @backup_name.setter
    def backup_name(self, arg):
        """
        Setter for backup_name
        """
        self._backup_name = arg

    def snapshot(self):
        """
        Using requests to generate a snapshot
        """
        try:
            self.log.debug("Creating Snapshot")
            put = requests.put("{}/_snapshot/{}/snapshot_{}".format(self.hostname, self.backup_name,
                                                                    datetime.now().strftime("%Y_%m_%dT%H_%M")),
                               data={'indices': 'graylog_0', 'ignore_unavailable': True, "include_global_state": False})
            put.raise_for_status()
        except Exception as e:
            loggin.error(e)
            raise SystemExit(e)
