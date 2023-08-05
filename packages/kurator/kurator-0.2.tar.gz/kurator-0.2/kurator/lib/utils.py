# -*- coding: utf-8 -*-
"""Utilities

Utilities module

Todo:

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from __future__ import print_function
import os
import time
import random
import hashlib

import exifread


def find_all_files(source, types):
    """Search for files of type and return list of absolute
    paths.

    source -- path to find files
    types -- tuple of types to search for
    """
    matches = []
    print(source)
    for root, _, files in os.walk(source):
        for filename in files:
            if filename.lower().endswith(types):
                matches.append(os.path.join(root, filename))
    return matches

def get_time_stamp():
    """Unix-like timestamp"""
    return str(int(time.time()))


def get_file_tags(path):
    """Get all exif tags from a file"""
    with open(path, 'rb') as file:
        raw_tags = exifread.process_file(file)
        tags = {
            'fileName': path,
            'dateTime': raw_tags['Image DateTime'].printable \
                if 'Image DateTime' in raw_tags \
                else 'NO_DATA_' + get_time_stamp() + str(random.randint(1, 1000)),
            'model': raw_tags['Image Model'].printable if 'Image Model' in raw_tags else 'unknown',
            'orientation': raw_tags['Image Orientation'].printable \
                if 'Image Orientation' in raw_tags \
                else 'unknown'
        }
        return tags

def generate_filename_from_meta(path):
    """Generate a filename from exif data.  Absolute path
    and extension included.
    """
    _, extension = os.path.splitext(path)
    return get_file_tags(path)['dateTime'].replace(':', '').replace(' ', '-') + extension.lower()

def generate_foldername_from_meta(path):
    """Generate folder name from exif data"""
    return get_file_tags(path)['dateTime'].replace(':', '').replace(' ', '-').lower()[:8]

def directory_exists(path):
    """Returns true if directory exists"""
    return os.path.isdir(path) and os.path.exists(path)

def create_directory(path):
    """Creates directory if it does not exist
    """
    if not directory_exists(path):
        print(path)
        os.makedirs(path)

def generate_md5(file):
    """Generate hashes"""
    return hashlib.md5(open(file, 'rb').read()).hexdigest()

def get_date_string_or(string):
    """If the string starts with 6 digits, that will be returned
    as a date in iso format.  Otherwise, todays date in iso
    format is returned.
    """
    if str(string[:5]).isdigit():
        return '{}-{}-{}'.format(string[:4], string[4:6], string[6:8])
    return time.strftime("%Y-%m-%d")

if __name__ == "__main__":
    pass
