nanoQC
======

Quality control tools for Oxford Nanopore sequencing data aiming to
replicate some of the plots made by fastQC.

|Twitter URL| |install with conda| |Code Health|

For an example see my blog `Gigabase or
gigabyte <https://gigabaseorgigabyte.wordpress.com/2017/06/15/per-base-sequence-content-and-quality-end-of-reads/>`__

INSTALLATION
------------

.. code:: bash

    pip install nanoQC

| or
| |install with conda|

::

    conda install -c bioconda nanoqc

USAGE
-----

::

    nanoQC [-h] [-v] [--outdir OUTDIR] fastq

    positional arguments:
      fastq            Reads data in fastq format.

    optional arguments:
      -h, --help       show this help message and exit
      -v, --version    Print version and exit.
      --outdir OUTDIR  Specify directory in which output has to be created.

STATUS
------

|Code Health|

.. |Twitter URL| image:: https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster
   :target: https://twitter.com/wouter_decoster
.. |install with conda| image:: https://anaconda.org/bioconda/nanoqc/badges/installer/conda.svg
   :target: https://anaconda.org/bioconda/nanoqc
.. |Code Health| image:: https://landscape.io/github/wdecoster/nanoQC/master/landscape.svg?style=flat
   :target: https://landscape.io/github/wdecoster/nanoQC/master
