=========
fiberless
=========

**Fiberless** monitors your internet connection
and when there is downtime, it is logged to a CSV file.

**Fiberless** was written by Nando Florestan in the Python 3 language.

Pull requests with additional features are very welcome.


Usage
=====

::

	# Print short usage message. Includes subcommand names.
	./fiberless.py

	# Print detailed help
	./fiberless.py --help

	# Print help about the "forever" subcommand -- it has its own arguments
	./fiberless.py forever --help

	# Monitor the network using the default options
	./fiberless.py forever
