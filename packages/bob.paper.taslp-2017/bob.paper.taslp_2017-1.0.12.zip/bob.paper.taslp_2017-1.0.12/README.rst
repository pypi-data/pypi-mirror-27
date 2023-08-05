.. vim: set fileencoding=utf-8 :
.. Tue  6 Dec 10:51:31 CET 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://beatubulatest.lab.idiap.ch/private/docs/bob/bob.paper.taslp_2017/stable/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: http://beatubulatest.lab.idiap.ch/private/docs/bob/bob.paper.taslp_2017/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.paper.taslp_2017/badges/master/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.taslp_2017/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.taslp_2017
.. image:: http://img.shields.io/pypi/v/bob.paper.taslp_2017.png
   :target: https://pypi.python.org/pypi/bob.paper.taslp_2017


=========================================================================================================
Reproducing results of paper submitted to IEEE/ACM Transactions on Audio, Speech, and Language Processing
=========================================================================================================

This package is part of the signal-processing and machine learning toolbox
Bob_ andit allows to reproduce the following paper::

    @inproceedings{Muckenhirntaslp_2017,
        author = {Muckenhirn, Hannah and Korshunov, Pavel and Magimai.-Doss, Mathew and Marcel, S{\'{e}}bastien},
        title = {Long Term Spectral Statistics for Voice Presentation Attack Detection,
        booktitle = {To appear in IEEE/ACM Transactions on Audio, Speech and Language Processing},
        year = {2017},
    }

If you use this package and/or its results, please cite the paper.

Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
