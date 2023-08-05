Évariste 🍼 Recursively compile and publish a dircetory tree
=============================================================

|sources| |pypi| |build| |coverage| |documentation| |license|

  On s'empressera de publier ses moindres observations pour peu qu'elles
  soient nouvelles et on ajoutera : « Je ne sais pas le reste. »

  -- Évariste Galois, 1831

.. note::

  As of 20/03/2015, this project is under active development, and is not usable
  yet.

Examples
--------

TODO Give links to the ikiwiki plugin and my website.

Stability
---------

Evariste is to be considered unstable at least until version `0.3.0 </spalax/evariste/milestones/2>`_.

I tried to make Evariste extendable throught plugins, but right now I only
wrote one plugin, whereas version `0.3.0 road map </spalax/evariste/milestones/2>`_ includes writing some other ones.  Thus,
version `0.3.0 </spalax/evariste/milestones/2>`_ can be seen as a way to test
the plugin system, find many bugs, rewrite parts of it, and deliver a (little
more) mature version of it.

Thus, things *will* change with version `0.3.0 </spalax/evariste/milestones/2>`_.

If you do want to write something using Evariste API (a plugin, for instance),
you can get in touch with me beforehand to discuss it, to prevent you from
writing code that will simply not work with version `0.3.0 </spalax/evariste/milestones/2>`_.

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/evariste/blob/master/CHANGELOG.md>`_.

Download and install
--------------------

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/evariste
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 setup.py install

* From pip::

    pip install evariste

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/evariste-<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://evariste.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html


.. |documentation| image:: http://readthedocs.org/projects/evariste/badge
  :target: http://evariste.readthedocs.io
.. |pypi| image:: https://img.shields.io/pypi/v/evariste.svg
  :target: http://pypi.python.org/pypi/evariste
.. |license| image:: https://img.shields.io/pypi/l/evariste.svg
  :target: http://www.gnu.org/licenses/agpl-3.0.html
.. |sources| image:: https://img.shields.io/badge/sources-evariste-brightgreen.svg
  :target: http://git.framasoft.org/spalax/evariste
.. |coverage| image:: https://git.framasoft.org/spalax/evariste/badges/master/coverage.svg
  :target: https://git.framasoft.org/spalax/evariste/builds
.. |build| image:: https://git.framasoft.org/spalax/evariste/badges/master/build.svg
  :target: https://git.framasoft.org/spalax/evariste/builds



