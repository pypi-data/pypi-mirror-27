pdfimpose 📕 Perform imposition of a PDF file
=============================================

|sources| |pypi| |build| |coverage| |documentation| |license|

    Imposition consists in the arrangement of the printed product’s pages on
    the printer’s sheet, in order to obtain faster printing, simplify binding
    and reduce paper waste (source: http://en.wikipedia.org/wiki/Imposition).


Examples
--------

* `2018 calendar <http://pdfimpose.readthedocs.io/en/latest/_downloads/calendar2018-impose.pdf>`_ (`source <http://pdfimpose.readthedocs.io/en/latest/_downloads/calendar2018.pdf>`__, see LaTeX source file in sources repository).
* `64 pages file <http://pdfimpose.readthedocs.io/en/latest/_downloads/dummy64-impose.pdf>`_ (`source <http://pdfimpose.readthedocs.io/en/latest/_downloads/dummy64.pdf>`__, generated using `dummypdf <http://git.framasoft.org/spalax/dummypdf>`_).

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/pdfimpose/blob/master/CHANGELOG.md>`_.

Download and install
--------------------

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/pdfimpose
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python setup.py install

* From pip::

    pip install pdfimpose

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/python<PYVERSION>-pdfimpose_<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://pdfimpose.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html


.. |documentation| image:: http://readthedocs.org/projects/pdfimpose/badge/?version=latest
  :target: http://pdfimpose.readthedocs.io
.. |pypi| image:: https://img.shields.io/pypi/v/pdfimpose.svg
  :target: http://pypi.python.org/pypi/pdfimpose
.. |license| image:: https://img.shields.io/pypi/l/pdfimpose.svg
  :target: http://www.gnu.org/licenses/gpl-3.0.html
.. |sources| image:: https://img.shields.io/badge/sources-pdfimpose-brightgreen.svg
  :target: http://git.framasoft.org/spalax/pdfimpose
.. |coverage| image:: https://git.framasoft.org/spalax/pdfimpose/badges/master/coverage.svg
  :target: https://git.framasoft.org/spalax/pdfimpose/builds
.. |build| image:: https://git.framasoft.org/spalax/pdfimpose/badges/master/build.svg
  :target: https://git.framasoft.org/spalax/pdfimpose/builds

