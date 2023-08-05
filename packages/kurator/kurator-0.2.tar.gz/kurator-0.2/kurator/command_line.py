import click
import kurator.kurator as k

# -*- coding: utf-8 -*-
"""Example Google style docstrings.

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
@click.group()
def cli():
    """Kurator helps manage photo and video dumps from a device
    to a photo library.

    A photo library is considered nothing more than a plain folder.
    """
    pass # pragma: no cover

@click.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('library', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def import_media(source, library):
    """ Imports media from a source into your library.

    Each image found in the source will be scanned for exif data.
    When copied to your library, it will be renamed using the date
    taken based on the exif data.

    Each image is placed into the library in a folder based on the date of its
    exif data.  If the folder doesn not already exist, it is created.

    If no exif data exists for the media file, a todays date combined with
    "NO_DATA" will be used as the filename.  A folder will be created using
    the same schema.

    SOURCE = the path of the media you want to import

    LIBRARY = the path of your photo library or any folder
    """
    k.import_media(source, library) # pragma: no cover


@click.command()
@click.argument('target', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def prune(target):
    """Removes duplicate files from the target

    Each file in the target directory is compared to each other file recursively
    in the same directory.

    If two files are the same, the duplicate is removed.

    TARGET = the path of the media file folder
    """
    k.prune(target) # pragma: no cover

@click.command()
@click.argument('target', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def fix_names(target):
    """ Rename all files in target using exif data (ie 20140201-165116.jpg)

    If no exif data exists for the media file, a todays date combined with
    "NO_DATA" will be used as the filename.

    TARGET = the path of the media file folder
    """
    k.fix_names(target) # pragma: no cover

def main():
    cli.add_command(import_media) # pragma: no cover
    cli.add_command(prune) # pragma: no cover
    cli.add_command(fix_names) # pragma: no cover
    cli() # pragma: no cover
