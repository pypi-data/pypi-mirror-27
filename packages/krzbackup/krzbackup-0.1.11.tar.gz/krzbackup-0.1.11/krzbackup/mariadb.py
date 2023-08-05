import logging
from distutils import dir_util
from os import path, stat
from subprocess import Popen, PIPE

from file import File_Backup
from service import Service


class MariaDB_Backup(Service, File_Backup):
    """
    MariaDB backup class
    """

    @property
    def username(self):
        """
        Username which is to be used for the Dump
        """
        return self._username

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
        return self._password

    @password.setter
    def password(self, arg):
        self._password = arg

    def __init__(self, username=None, password=None, source_location=None, target_location=None):
        """
        Initial checks upon object creation
        """

        self.log = logging.getLogger('backup.mariadb')

        if username:
            self.username = username

        if password:
            self.password = password

        if source_location:
            self.source_location = source_location

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

        dump_file = self.target_location + "/db_dump.sql"

        if path.isfile(dump_file) and stat(dump_file).st_size > 0:
            try:
                fo = open(dump_file, 'rw+')
                fo.truncate()
                fo.close()
            except Exception as e:
                raise

        if not path.isfile(dump_file):
            try:
                open(dump_file, 'w')
            except Exception as e:
                self.log.error(e)
                raise

        if self.username is None or self.password is None:
            msg = "username or password is not set, can not do a backup without them"
            self.log.error(msg)
            raise ValueError(msg)
        else:
            self.log.debug(
                "/usr/bin/mysqldump -v --all-databases -u {} -p{} > {}".format(self.username, self.password, dump_file))
            mysqldump = Popen(
                "/usr/bin/mysqldump --all-databases -u {} -p{} > {}".format(self.username, self.password, dump_file),
                shell=True, stdout=PIPE, stderr=PIPE)

            self.log.debug("Dumping MariaDB Databases")
            output = mysqldump.communicate()[0]
            self.log.info(output)
            mysqldump.wait()

    def binary_backup(self):
        """
        Copying binary Logs to backup location
        """

        self.log.debug("Running the Binary Backup")
        if find_procs_by_name("mysql"):
            self.log.debug("found a running mysql process and trying to stop it")
            stop_service("mariadb.service")
            if self.retry > 0:
                msg = "There is still a MySQL process running, it has to be stopped for the copy to work properly"
                logging.error(msg)
                raise Exception(msg)
            self.retry += 1
            self.binary_backup()

        self.log.debug("Copying binary logs")
        dir_util.copy_tree(self.source_location, self.target_location)
