from datetime import datetime, timedelta
from os import remove
from os import walk
from pprint import pformat


class retention():
    """
    Class that checks the retention state of the backups and deletes them
    """

    def delete(self, path, retentiontime):
        def check(path, retentiontime):
            """
            returns list of all backups that are out of retention
            """

            diff = datetime.today() - timedelta(days=retentiontime)

            retentionlist = []

            for (dirpath, dirnames, filenames) in walk(path):
                for filename in filenames:

                    file_date = datetime.strptime(path.splitext(filename))

                    if file_date < diff and "tar.gz" in filename:
                        retentionlist.append(filename)

            return retentionlist

        retentionlist = check(path=path, retentiontime=retentiontime)

        for (dirpath, dirnames, filenames) in walk(path):
            for filename in filenames:
                if filename in retentionlist:
                    remove(filename)

        retentionlist = check(path=path, retentiontime=retentiontime)

        if retentionlist:
            raise BaseException("found backups that still exists{}".format(pformat(retentionlist)))
        else:
            return True
