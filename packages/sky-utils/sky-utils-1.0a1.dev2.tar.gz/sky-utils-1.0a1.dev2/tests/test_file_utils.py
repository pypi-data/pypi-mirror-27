import tempfile
import unittest
import shutil
import os
import logging

from os.path import basename

from sky.utils.file import FileUtils

__author__ = 'muhammet@macit.org'

logger = logging.getLogger(__name__)


class TestFileUtils(unittest.TestCase):
    def setUp(self):
        if len(logger.handlers) < 1:
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        logger.info("created test folder: '%s'" % self.test_dir)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
        logger.info("deleted test folder: '%s'" % self.test_dir)

    def test__list_files_no_filter(self):
        files = ["assd", "assd2"]
        [open(os.path.join(self.test_dir, file), 'a').close() for file in files]
        list_files = FileUtils.list_files(self.test_dir)
        [self.assertEquals(basename(list_files[idx]), files[idx]) for idx in range(len(files))]
        [self.assertEquals(list_files[idx], os.path.join(self.test_dir, files[idx])) for idx in range(len(files))]

    def test__list_files_no_filter_no_full_path(self):
        files = ["assd", "assd2"]
        [open(os.path.join(self.test_dir, file), 'a').close() for file in files]
        list_files = FileUtils.list_files(self.test_dir, None, False)
        [self.assertEquals(list_files[idx], files[idx]) for idx in range(len(files))]

    def test__list_files_with_filter(self):
        files = ["assd.txt", "assd2.txt"]
        [open(os.path.join(self.test_dir, file), 'a').close() for file in files]
        list_files = FileUtils.list_files(self.test_dir, r'.+\.txt')
        [self.assertEquals(basename(list_files[idx]), files[idx]) for idx in range(len(files))]

    def test__list_files_with_filter_mixed(self):
        files = ["assd.txt", "assd2.txt", "assd3"]
        filtered_files = ["assd.txt", "assd2.txt"]
        [open(os.path.join(self.test_dir, file), 'a').close() for file in files]
        list_files = FileUtils.list_files(self.test_dir, r'.+\.txt')
        [self.assertEquals(basename(list_files[idx]), filtered_files[idx]) for idx in range(len(filtered_files))]
