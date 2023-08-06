.. Copyright (C) 2013 Branko Majic

   This file is part of Django Conntrackt documentation.

   This work is licensed under the Creative Commons Attribution-ShareAlike 3.0
   Unported License. To view a copy of this license, visit
   http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative
   Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


Release Notes
=============


0.3.0
-----

Breaking changes:

* Package now has hard dependency on more specific versions of
  requirements in order to ensure it is not used with incompatible
  variants (for example, Django has been fixated to version
  1.5.x). This could cause some issues if application is used with
  newer Django versions etc.
  [ `CONNT-28 <https://projects.majic.rs/conntrackt/issues/CONNT-28>`_ ]

New features/improvements:

* A lot of cleanup was performed to make it easier to handle
  development process etc. These are mostly internal changes, except
  for small documentation fixes.
  [ `CONNT-28 <https://projects.majic.rs/conntrackt/issues/CONNT-28>`_ ]

Bug-fixes:

* Documentation links have been updated to point to new Read The Docs
  domain.
  [ `CONNT-27 <https://projects.majic.rs/conntrackt/issues/CONNT-27>`_ ]


0.2
---

This release contains mainly some usability features, and some minor
bug-fixes. No changes to database schema were made.

New features:

* Tabluar representation of project communications, with colour-coding matching
  the diagram. [ `CONNT-17 <https://projects.majic.rs/conntrackt/issues/CONNT-17>`_ ]
* Simple search functionality, including search suggestions if JavaScript is
  enabled. [ `CONNT-19 <https://projects.majic.rs/conntrackt/issues/CONNT-19>`_,
  `CONNT-23 <https://projects.majic.rs/conntrackt/issues/CONNT-23>`_ ]
* Removing an object will list all related objects that will get removed as
  well. [ `CONNT-20 <https://projects.majic.rs/conntrackt/issues/CONNT-20>`_ ]

Bug fixes:

* Generates valid XHTML5 code now. [ `CONNT-24 <https://projects.majic.rs/conntrackt/issues/CONNT-24>`_ ]


0.1
---

Initial relase of Django Conntrackt. Contains full support for:

* Managing application data.
* Generation of iptables rules.
* Generation of communication diagram.
* Full user documentation.
