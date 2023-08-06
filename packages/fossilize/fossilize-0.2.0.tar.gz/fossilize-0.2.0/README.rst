*********
Fossilize
*********
Append repository, commit, and date metadata to a file or script.  I use this 
command for scientific notebooking; it helps me keep track of which versions of 
my protocols I used for which experiments.

.. image:: https://img.shields.io/pypi/v/fossilize.svg
   :target: https://pypi.python.org/pypi/fossilize

.. image:: https://img.shields.io/pypi/pyversions/fossilize.svg
   :target: https://pypi.python.org/pypi/fossilize

.. image:: https://img.shields.io/travis/kalekundert/fossilize.svg
   :target: https://travis-ci.org/kalekundert/fossilize

.. image:: https://img.shields.io/coveralls/kalekundert/fossilize.svg
   :target: https://coveralls.io/github/kalekundert/fossilize?branch=master

Installation
============
Install `fossilize` via pip::

   $ pip3 install fossilize

Usage
=====
Run the `fossilize` command on the file or script you want to record::

   $ fossilize my_protocol.txt
   Command recorded to: 20171024_my_protocol.txt

If the script takes any arguments, simply supply them after the command::

   $ fossilize my_script.py spam eggs
   Command recorded to: 20171024_my_script.txt

