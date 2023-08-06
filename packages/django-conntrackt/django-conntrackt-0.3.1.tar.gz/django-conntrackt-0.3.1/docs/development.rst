.. Copyright (C) 2017 Branko Majic

   This file is part of Django Conntrackt documentation.

   This work is licensed under the Creative Commons Attribution-ShareAlike 3.0
   Unported License. To view a copy of this license, visit
   http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative
   Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


.. _development:

Development
===========

This section provides an overview of how to take care of Django
Conntrackt development, including instructions on how to get started,
procedures, and common tools.

Instructions are primarily aimed at use of Debian Stretch (as of time
of this writing). If you are running a different distribution or OS,
you will need to modify the instructions to suit your environment.


Preparing development environment
---------------------------------

Perform the following steps in order to prepare development
environment:

1. Ensure that the following system packages are available on the
   system:

   - `Python 2.7.x <https://www.python.org/>`_
   - `Graphviz <https://graphviz.org/>`_
   - `virtualenv <https://pypi.python.org/pypi/virtualenv>`_
   - `virtualenvwrapper
     <https://virtualenvwrapper.readthedocs.io/en/latest/>`_

   Under Debian GNU/Linux it should be easy to install all the
   necessary dependencies with command (provided you have sudo set-up,
   otherwise run command as ``root`` without ``sudo``):

   .. warning::
      Don't forget to start a new shell in order to be able to use the
      virtualenvwrapper.

   ::

     sudo apt-get install python2.7 graphviz mercurial virtualenv virtualenvwrapper

2. Clone the application repository::

     mkdir ~/projects/
     hg clone https://code.majic.rs/conntrackt/ ~/projects/conntrackt

3. Set-up a new virtual environment::

     mkvirtualenv -a ~/projects/conntrackt/ conntrackt

4. Install required packages in the virtual environment::

     workon conntrackt && pip install -r ~/projects/conntrackt/requirements/development.txt


Development/test Django project
-------------------------------

*Django Contrackt* comes with a test Djanbo project which can be used
out-of-the-box once database has been initialised.

Once the development environment has been set-up, you can set-up its
database with::

  workon conntrackt
  cd testproject/
  ./manage.py syncdb
  ./manage.py migrate

Once the database has been set-up, run the development server with::

  workon conntrackt
  cd testproject/
  ./manage.py runserver

To access the application via started development server, simply point
your browser to http://localhost:8000/conntrackt/ .


Running tests
-------------

The application is well covered with various (primarily unit) tests,
and the tests can be easily run via the supplied test/development
projects. Once the development environment has been set-up, tests can
be easily run with::

  workon conntrackt
  cd ~/projects/conntrackt/testproject/
  ./manage.py test conntrackt


Keeping installation and development requirements up-to-date
------------------------------------------------------------

There are two different types of (``pip``) requirements to keep in
mind while developing the application:

- Package installation requirements, specified in ``setup.py``.
- Development requirements, maintained in dedicated requiremnts files.

Distinction exists in order to allow faster start-up with the
development environment, as well as to ensure that during the
installation of package no side-effects are encountered due to
dependencies being too lax or untested.

Base installation requirements are preserved within the ``setup.py``
configuration script and are updated on as-needed basis by
hand. Packages within are pinned to stable releases required by
Conntrack to properly operate. For example, Django version is fixed to
reduce chance of running application against a wrong Django version.

Development requirements duplicate the information stored within
``setup.py``, but also introduce some addtional tools required for
running tests, or tools that simply make the life easier.

Development requirements are kept up-to-date via ``pip-compile`` from
`pip-tools <https://pypi.python.org/pypi/pip-tools/>`_.

The input into the tool are the ``.in`` files located within the
requirements sub-directory:

- ``base.in``, which reflects requirements outlined within the
  ``setup.py``.
- ``development.in``, which includes the base requirements, as well as
  additional ones needed for the normal development process.
- ``test.in``, which includes the base requirements, as well as
  additional ones needed to run the tests.

These input files are maintained by hand as well. However, the
resulting requirements ``.txt`` files are updated via the
``pip-compile`` tool. In order to sync changes in ``.in`` files, or to
update the requirements, simply run commands::

  workon conntrackt
  pip install pip-tools
  pip-compile --upgrade ./requirements/development.in
  pip-compile --upgrade ./requirements/test.in

Afterwards you can commit the changes via standard Mercurial tools
(make sure the new requirements do not break the development/testing).

Should you wish to, you can also opt to use the ``pip-sync`` utility
to keep your development environment in sync with the requirements
file. Just keep in mind that it will uninstall any package not listed
in requirements, and that it will force package versions from the
requirements file::

  workon conntrackt
  pip-sync ./requirements/development.txt
