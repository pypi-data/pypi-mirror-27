import os
import re

__author__ = 'muhammet@macit.org'


class FileUtils(object):
    @staticmethod
    def list_files(folder, filter_regex=None, full_path=True):
        """
        List files based on given folder path, can return regex filtered result and full path of listed files on demand
        :param folder: folder path to be listed
        :param filter_regex: only matched file names will be return based on this given regex
        :param full_path: this parameter provides listing all of files with their full paths
        :return: list of file paths at given folder
        """
        file_paths = []
        files_names = sorted(os.listdir(folder))
        for file_name in files_names:
            if os.path.exists(os.path.join(folder, file_name)):
                x = (os.path.join(folder, file_name) if full_path else file_name)
                if filter_regex:
                    if re.match(filter_regex, file_name):
                        file_paths.append(x)
                else:
                    file_paths.append(x)
        return file_paths
