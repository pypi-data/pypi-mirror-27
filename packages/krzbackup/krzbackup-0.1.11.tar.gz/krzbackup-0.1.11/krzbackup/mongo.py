import logging
from subprocess import Popen, PIPE

from file import File_Backup
from service import Service


class MongoDB_Backup(Service, File_Backup):
    """
    MongoDB Backup class
    """

    _username = None
    _password = None

    @property
    def username(self):
        """
        Username which is to be used for the Dump
        """
        if self._username:
            return self._username
        else:
            return None

    @username.setter
    def username(self, arg):
        """
        Setter for username
        """
        self._username = arg

    @property
    def password(self):
        """
        Password which is to be used for the Dump
        """
        if self._password:
            return self._password
        else:
            return None

    @password.setter
    def password(self, arg):
        self._password = arg

    def __init__(self, username=None, password=None, target_location=None):
        """
        Initial checks upon object creation
        """

        self.log = logging.getLogger('backup.mongodb')

        if username:
            self.username = username

        if password:
            self.password = password

        if target_location:
            self.target_location = target_location
        else:
            msg = 'target_location not set.'
            self.log.error(msg)
            raise ValueError(msg)

    def dump_backup(self):
        """
        Handing dumping the DB to a subprocess
        """
        if self.find_procs_by_name("mongodb"):
            self.log.debug("found a running mongoDB process and trying to stop it")
            stop_service("mongodb.service")
            if self.retry > 0:
                msg = "There is still a MongoDB process running, it has to be stopped for the copy to work properly"
                logging.error(msg)
                raise Exception(msg)
            self.retry += 1
            self.dump_backup()

        if self.username and self.password:
            self.log.debug("Trying to run MongoDump without Credentials")
            dump = Popen("mongodump -o {}".format(self.target_location),
                         stdout=PIPE, stdin=PIPE)
        else:
            self.log.debug("Trying to run MongoDump with Credentials")
            dump = Popen("mongodump -u {} -p {} -o {}".format(self.username, self.password, self.target_location),
                         stdout=PIPE, stdin=PIPE)

        output = dump.communicate()[0]
        dump.wait()
        self.log.debug(output)
