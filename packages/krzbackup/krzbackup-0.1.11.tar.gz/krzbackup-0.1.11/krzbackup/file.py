import logging
import os
import shutil
from distutils import dir_util


class File_Backup(object):
    """
    File Backup class
    """

    @property
    def target_location(self):
        """
        Target Location to where we want to copy or dump Data
        """
        return self._target_location

    @target_location.setter
    def target_location(self, arg):
        """
        Setter for target_location
        """
        if os.path.isdir(arg):
            self._target_location = arg
        else:
            msg = "Target Directory does not exists"
            logging.error(msg)
            raise ValueError(msg)

    @property
    def source_location(self):
        """
        Source location
        """
        return self._source_location

    @source_location.setter
    def source_location(self, arg):
        """
        Setter for source_location
        """
        if os.path.isdir(arg):
            self._source_location = arg
        else:
            msg = "Target Directory does not exists"
            logging.error(msg)
            raise ValueError(msg)

    def __init__(self):
        super(File_Backup, self).__init__()

    def file_backup(self, file_exclusion=[]):
        """
        Backing up files from source to target location
        """
        files_in_location = self.list_files

        if not file_exclusion:
            logging.debug("Working without exclusions")
            dir_util.copy_tree(self.source_location, self.target_location, preserve_symlinks=1)
        else:
            logging.debug("Working with exclusions: {}".format(vars(files_in_location)))
            for file in files_in_location:
                logging.debug("Working with file {}".format(file))
                for exclusion in file_exclusion:
                    if not exclusion in file:
                        logging.debug("Copying file: {}".format(file))
                        shutil.copyfile(self.source_location + file, self.target_location + file)

    def list_files(self, location):
        """
        List files for given location and return dictionary, non recursive
        """
        logging.debug("Generating List of Directory: {}".format(location))
        return os.listdir(location)
