Welcome to `dummypdf`'s documentation!
======================================

This tool can produce dummy PDF files. They can be used to test software
manipulating such PDF files.

The produced files contain:

- a big page number;
- a rectangle around the page, and a cross across the whole page.

The color, page format and number of pages can be configured.

Examples:

- One page A4 paper: :download:`example1 <examples/example1.pdf>`
- Six pages, a third of an A4 paper: :download:`example2 <examples/example2.pdf>`
- A pdf with different page formats: :download:`different.pdf <examples/different.pdf>`

Download and install
--------------------

See the `project main page <http://git.framasoft.org/spalax/dummypdf>`__, and
`changelog <https://git.framasoft.org/spalax/dummypdf/blob/master/CHANGELOG.md>`_.

Usage
-----

Here are the command line options for `dummypdf`.

.. argparse::
    :module: dummypdf.__main__
    :func: commandline_parser
    :prog: dummypdf

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
