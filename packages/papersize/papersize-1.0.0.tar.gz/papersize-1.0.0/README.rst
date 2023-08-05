papersize 📏 Paper size related tools
====================================

|sources| |pypi| |build| |coverage| |documentation| |license|

This module provides tools to manipulate paper sizes, that is:

- a dictionary of several named standard names (e.g. A4, letter) , with their
  respective sizes (with and height);
- functions to convert sizes between units;
- functions to manipulate paper orientation (portrait or landscape);
- tools to parse paper sizes, so that you do not have to worry about the format
  of paper sizes provided by your user, it being `a4` or `21cm x 29.7cm`.

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/papersize/blob/master/CHANGELOG.md>`_.

Install
-------

This module is compatible with both python 2 and 3.

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/papersize
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

      python setup.py install

* From pip::

    pip install papersize

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/python-papersize-<VERSION>_all.deb

Test
----

* Current python version::

    python setup.py test

* All supported python versions (using `tox <http://tox.testrun.org>`_)::

    tox

Documentation
-------------

The documentation is available on `readthedocs <http://papersize.readthedocs.io>`_.  You can build it using::

  cd doc && make html

.. |documentation| image:: http://readthedocs.org/projects/papersize/badge
  :target: http://papersize.readthedocs.io
.. |pypi| image:: https://img.shields.io/pypi/v/papersize.svg
  :target: http://pypi.python.org/pypi/papersize
.. |license| image:: https://img.shields.io/pypi/l/papersize.svg
  :target: http://www.gnu.org/licenses/gpl-3.0.html
.. |sources| image:: https://img.shields.io/badge/sources-papersize-brightgreen.svg
  :target: http://git.framasoft.org/spalax/papersize
.. |coverage| image:: https://git.framasoft.org/spalax/papersize/badges/master/coverage.svg
  :target: https://git.framasoft.org/spalax/papersize/builds
.. |build| image:: https://git.framasoft.org/spalax/papersize/badges/master/build.svg
  :target: https://git.framasoft.org/spalax/papersize/builds

