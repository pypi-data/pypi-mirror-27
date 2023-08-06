optioncomplete
==============

Description
-----------

Command line tab completion for optparse


Installation
------------

.. code-block:: bash

	$ sudo pip3 install optioncomplete**


Example python code
-------------------

.. code-block:: python

	import sys
	from optparse import OptionParser
	from optioncomplete import autocomplete
	...
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
		          help="write report to FILE", metavar="FILE")
	parser.add_option("-q", "--quiet",
		          action="store_false", dest="verbose", default=True,
		          help="don't print status messages to stdout")
	autocomplete(parser,sys.argv[0])
	(options, args) = parser.parse_args()


Installation and usage in command line
--------------------------------------

`Optioncomplete youtube <https://www.youtube.com/watch?v=FuSK5cs1ijo>`_
