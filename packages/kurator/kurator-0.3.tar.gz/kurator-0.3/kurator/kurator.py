"""Kurator.py

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import os
import sys
import filecmp
import logging
from shutil import copy2 as copy_file, SameFileError

from kurator.lib import utils as u

class NoError(logging.Filter):
    """Only reports items not in Warning, Error, and Critical
    """
    def filter(self, record):
        return not record.levelname in ['WARNING', 'ERROR', 'CRITICAL']

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

HANDLER_STDOUT = logging.StreamHandler(sys.stdout)
HANDLER_STDOUT.setLevel(logging.WARNING)
HANDLER_STDOUT.setFormatter(FORMATTER)
HANDLER_STDOUT.addFilter(NoError())

HANDLER_STDERR = logging.StreamHandler()
HANDLER_STDERR.setLevel(logging.INFO)
HANDLER_STDERR.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER_STDOUT)
LOGGER.addHandler(HANDLER_STDERR)

def import_media(source, library):
    """ Imports media from source into library """

    files = u.find_all_files(source, ('.jpg', '.mp4', '.mov'))
    print('Processing {} photos'.format(len(files)))
    for idx, file_item in enumerate(files):
        folder_name = os.path.join(library, u.generate_foldername_from_meta(file_item))
        file_name = u.generate_filename_from_meta(file_item)
        u.create_directory(folder_name)

        if os.path.exists(os.path.join(folder_name, file_name)):
            file_name = '{}_DUP_{}{}'.format(file_name, u.get_time_stamp(), idx)
        copy_file(file_item, os.path.join(folder_name, file_name))

def prune(target):
    """Removes duplicate files from the target"""

    files = u.find_all_files(target, ('.jpg', '.mp4', '.mov'))
    LOGGER.info('Scanning %s files...', len(files))

    to_remove = []
    for idx, primary_file in enumerate(files):
        for comparing_file in files[idx + 1: len(files)]:
            if filecmp.cmp(primary_file, comparing_file):
                LOGGER.info("duplicates found: %s and %s are equal; slating %s for removal",
                            primary_file, comparing_file, comparing_file)
                to_remove.append(comparing_file)

    LOGGER.info('Removing %s files...', len(to_remove))
    for file_item in to_remove:
        if os.path.isfile(file_item):
            LOGGER.info('removing file_item %s', file_item)
            os.remove(file_item)
        else:
            print('file_item {} previously removed'.format(file_item))

def fix_names(target):
    """ Checks that the name of the file_item matches the exif data
    contained in the file_item
    """
    raw_files = u.find_all_files(target, ('.jpg', '.mp4', '.mov'))
    files = (file for file in raw_files)
    print('Scanning {} photos'.format(len(raw_files)))
    for idx, file_item in enumerate(files):
        folder_name = os.path.join(target, u.generate_foldername_from_meta(file_item))
        file_name = u.generate_filename_from_meta(file_item)
        u.create_directory(folder_name)

        if os.path.exists(os.path.join(folder_name, file_name)):
            file_name = '{}_DUP_{}{}'.format(file_name, u.get_time_stamp(), idx)
        copy_file(file_item, os.path.join(folder_name, file_name))
        os.remove(file_item)

if __name__ == "__main__":
    pass
