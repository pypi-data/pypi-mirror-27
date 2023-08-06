import os
import errno
import shutil
import stat
"""A set of utilities to perform file operations"""


class FileHelpers:

    @staticmethod
    def makeSurePathExists(path):
        """ create the path hierarchy to make sure it finally exists

        raises exception only if the hierarchy can not be created.
        No exception raised if it already exists
        """
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    @staticmethod
    def onRemoveError(action, name, exc):
        """error handler for shutil.rmtree, will try to remove 'readonly' attribute from files"""
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    @staticmethod
    def makeSurePathDoesNotExists(path):
        """ make sure the given directory is empty and does not exists.

        raises exception only if it fails emptying the directory
        No exception raised if it does not exist or if it is not empty
        """
        try:
            shutil.rmtree(path, onerror=FileHelpers.onRemoveError)
        except OSError as exception:
            if exception.errno != errno.ENOENT:
                raise


    @staticmethod
    def remove(filePath):
        """ removes the given file.  Does not raises any exception if the file does not exist.

        raises exception only if the file exist and can not be deleted
        """
        try:
            os.remove(filePath)
        except OSError as exception:
            if exception.errno != errno.ENOENT:
                raise