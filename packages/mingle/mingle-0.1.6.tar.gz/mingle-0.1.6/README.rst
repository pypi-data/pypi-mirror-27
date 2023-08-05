Mingle
------

Mingle is a library and command line tool to allow you to read from many log files, line by line in chronological order.

Introduction
============

Mingle uses the python-dateutil module to flexibly attempt to parse the first part of each line as a datetime, and
provides a generator to access the lines in total chronological order, across the input files.

It also offers a function to conveniently print the lines out in chronological order, optionally marking which files
the lines come from.

A command line utility 'mingle' is also provided, to print the log file lines in chronological order from the shell.

Usage:
======

To access a generator that will return lines from multiple log files in chronological order::

    >>> from mingle import mingled
    >>> files = ['webserver-log', 'db-log', 'firewall-log']
    >>> for line, filename in mingled(files):
    >>>     print("The line: " + line)
    >>>     print("From file:" + filename)


To conveniently print the lines to stdout::

    >>> import mingle
    >>> files = ['webserver-log', 'db-log', 'firewall-log']
    >>> mingle.cat(files)


To print the usage of the command line interface::

    user@localhost:~$ mingle -h
    usage: mingle [-h] [-q] files [files ...]

    Inter-mingle the contents of several log files by date stamp.

    positional arguments:
      files        the files to intermingle

    optional arguments:
      -h, --help   show this help message and exit
      -q, --quiet  strip the filename annotations from the output
