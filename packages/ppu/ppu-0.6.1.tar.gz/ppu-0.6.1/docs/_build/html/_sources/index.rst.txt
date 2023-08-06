.. ppu documentation master file, created by
   sphinx-quickstart on Sat Apr 15 20:37:34 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Portable Python Utilities
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   news

.. highlight:: none

Command line
------------

cmp.py
~~~~~~

Compare two files.

Usage::

    cmp.py [-i] [-s --silent --quiet] file1 file2

Options::

    -i, --inhibit-progress-bar
                                 inhibit progress bar
    -s, --silent, --quiet
                                 be silent (implied -i)


remove-old-files.py
~~~~~~~~~~~~~~~~~~~

Remove old files. It's a portable replacement for
`find start_dir -type f -mtime +31 -delete`.

Usage::

    remove-old-files.py [-e] -o days start_dir

Options::

    -e, --empty-dirs
                           remove empty directories
    -o days, --older days
                           remove files older than this number of days;
                           this is a required option

rm.py
~~~~~

Remove files or directories. Ask interactively to remove read-only files or
directories.

Usage::

    rm.py [-r] name1 [name2...]

Options::

    -r, --recursive
                        recursively remove directories
    -f', --force
                        force (ignore non-existing files and errors)


which.py
~~~~~~~~

Find a program in PATH and print full path to it.

Usage::

    which.py program

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
