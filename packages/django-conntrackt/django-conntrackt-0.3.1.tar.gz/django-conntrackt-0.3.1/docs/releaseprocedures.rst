Release procedures
==================

This section documents various release procedures. This includes:

- General versioning schema principles.
- General backporting principles.
- Releases of major versions.
- Releases of minor versions.
- Releases of patch versions.
- Writing release notes.
- Release issue template.


Versioning schema
-----------------

*Django Conntrackt* project employs `semantic versioning
<http://semver.org/>`_ schema. In short:

- Each version is composed of major, minor, and patch number. For example, in
  version ``1.2.3``, ``1`` is the major, ``2`` is the minor, and ``3`` is the
  patch number.
- Major number is bumped when making a backwards incompatible
  change. I.e. anything that depends on *Django Conntrackt* may need to make
  changes in order to keep working correctly.
- Minor number is bumped when new features or changes are made without breaking
  backwards compatibility. I.e. if you were using version ``1.2.3``, you should
  be safe to upgrade to version ``1.3.0`` without making any changes to whatever
  is using *Django Conntrackt*.
- Patch number is bumped when making purely bug-fix backwards compatible
  changes. Patch releases are generally more likely to remain stable simply due
  to limited scope of changes (new features can sometimes introduce unexpected
  bugs). It shouild be noted that due to relatively limited resources I have
  (plus, the roles are mainly used by myself :), patch releases might be a bit
  more scarce, and I might opt for going for minor release instead to reduce
  amount of work needed (backporting and releasing).

In addition to versioning schema, *Django Conntrackt* employs a specific
nomenclature for naming the branches:

- All new development and bug-fixing uses ``default`` branch as the base.
- Patch releases are based off the maintenance branches. Mainteance branches are
  named after the ``MAJOR`` and ``MINOR`` number of the version. For example, if
  a new release is made with version ``1.2.0``, the corresponding branch that is
  created for maintenance will be named ``1.2`` (notice the absence of ``.0`` at
  the end).


Writing release notes
---------------------

Release notes should be updated in relevant branches as the issues are
getting resolved. The following template should be used when
filling-up the release notes (take note the links to issues are kept
on separate page)::

  VERSION
  -------

  GENERAL DESCRIPTION

  Breaking changes:

  * DESCRIPTION
    [ `CONNT-NUMBER <https://projects.majic.rs/conntrackt/issues/CONNT-NUMBER>`_ ]

  New features/improvements:

  * DESCRIPTION
    [ `CONNT-NUMBER <https://projects.majic.rs/conntrackt/issues/CONNT-NUMBER>`_ ]

  Bug-fixes:

  * DESCRIPTION
    [ `CONNT-NUMBER <https://projects.majic.rs/conntrackt/issues/CONNT-NUMBER>`_ ]


Release issue template
----------------------

The following template can be used when creating the issue for a
release in the issue tracker:

- Set *subject* to ``Release version MAJOR.MINOR.PATCH``.
- Set *description* to::

    Release version MAJOR.MINOR.PATCH. Release should be done
    according to release procedures outlined in offline documentation.


Backporting fixes
-----------------

From time to time it might become useful to apply a bug-fix to both
the default development branch, and to maintenace branch.

When a bug is discovered in one of the roles (or maybe documentation), and it
should be applied to maintenance branch as well, procedure is as follows:

1. Create a new bug report in `issue tracker
   <https://projects.majic.rs/conntrackt>`_. Target version should be
   either the next minor or next major release (i.e. whatver will get released
   from the default development branch).

2. Create a copy of the bug report, modifying the issue title to include phrase
   ``(backport to MAJOR.MINOR)`` at the end, with ``MAJOR`` and ``MINOR``
   replaced with correct versioning information for the maintenance
   branch. Make sure to set correct target version (patch release).

3. Resolve the bug for next major/minor release.

4. Reslove the bug in maintenace branch by backporting (using graft if
   possible) the fix into maintenace branch. Make sure to reword the
   commit message (to reference the backport issue) .


Releasing new version
---------------------

The following procedure is applicable to both major/minor and patch
releases, with any relevant differences pointed out in the individual
steps.

Perform the following steps in order to release a new version:

1. Verify that there are no outstanding issues blocking the release.

2. Prepare release environment:

   1. Switch to the project Python virtual environment::

        workon conntrackt

   2. Set release version, and set issue associated with making the
      release::

        VERSION="MAJOR.MINOR.PATCH"
        ISSUE="CONNT-NUMBER"
        BRANCH="${VERSION%.*}"

   3. Verify the information has been set correctly::

        echo "[$ISSUE] $BRANCH -> $VERSION"

3. If this is a new major/minor release, prepare the maintenance
   branch:

   .. warning::
      Make sure **not** to run these steps when making a patch release!

   1. Create the maintenance branch::

        hg branch "$BRANCH"

   2. Update versioning information in documentation and setup
      script::

        sed -i -e "s/^version = .*/version = '${BRANCH}-maint'/" docs/conf.py
        sed -i -e "s/^    version=.*/    version='${BRANCH}-maint',/" setup.py
        sed -i -e "s/^dev$/${BRANCH}-maint/" docs/releasenotes.rst

   3. Fix the title underline for version string in
      ``docs/releasenotes.rst``.

   4. Show differences before committing::

        hg diff

   5. Commit the changes::

        hg commit -m "$ISSUE: Creating maintenance branch ${BRANCH}."

4. Ensure you are on the maintenance branch:

   1. Switch to maintenance branch::

        hg update "$BRANCH"

   2. Verify the switch::

        hg branch

5. Create release commit:

   .. warning::
      Make sure not to push changes at this point, since the relesae
      commit must be tested first.

   1. Update versioning information in documentation and setup
      script::

        sed -i -e "s/^version = .*/version = '${VERSION}'/" docs/conf.py
        sed -i -e "s/^    version=.*/    version='${VERSION}',/" setup.py
        sed -i -e "s/^${BRANCH}-maint$/${VERSION}/" docs/releasenotes.rst

   2. Fix the title underline for version string in
      ``docs/releasenotes.rst``.

   3. Show differences before committing::

        hg diff

   4. Commit the changes::

        hg commit -m "$ISSUE: Releasing version ${VERSION}."

6. Verify release behaves as expected:

   1. Verify that documentation builds and looks correct::

        (cd docs/; make clean html; firefox _build/html/index.html)

   2. Run tests::

        (cd testproject; python manage.py test)

   3. Build source distribution package, verifying no errors are
      reported::

        python setup.py sdist

   4. Test the quick-start instructions to ensure they are still
      applicable. When installing the package, make sure to use the
      source distribution package from previous step.

   5. Correct any outstanding issues prior to proceeding further, and
      repeat the test cycle for any sort of change, ammending the
      previous commit if possible (instead of creating new ones).

7. Push release to PyPI:

   1. Tag the release::

        hg tag "$VERSION"

   2. Push the (tested) built source distribution::

        python setup.py sdist upload

8. Clean-up the maintenance branch:

   1. Start a new release notes section in ``docs/releasenotes.rst``::

        sed -i "/^Release Notes$/{N;s/$/\n\n\n${BRANCH}-maint\n-----------/}" docs/releasenotes.rst

   2. Update versioning information in documentation and setup
      script::

        sed -i -e "s/^version = .*/version = '${BRANCH}-maint'/" docs/conf.py
        sed -i -e "s/^    version=.*/    version='${BRANCH}-maint',/" setup.py

   3. Fix the title underline for version string in
      ``docs/releasenotes.rst``.

   4. Show differences before committing::

        hg diff

   5. Commit the changes::

        hg commit -m "$ISSUE: Bumping version back to maintenance."

9. Clean-up the default branch if you have just released a new
   major/minor version:

   .. warning::
      Make sure **not** to run these steps when making a patch release!

   1. Switch to default development branch::

        hg update default

   2. Verify the switch::

        hg branch

   3. Update versioning information in release notes::

        sed -i -e "s/^dev$/${VERSION}/" docs/releasenotes.rst

   4. Start a new release notes section in ``docs/releasenotes.rst``::

        sed -i "/^Release Notes$/{N;s/\$/\n\n\ndev\n---/}" docs/releasenotes.rst

   5. Fix the title underlines for version strings in
      ``docs/releasenotes.rst``.

   6. Show differences before committing::

        hg diff

   7. Commit the changes::

        hg commit -m "$ISSUE: Starting new release notes in default development branch."

10. Wrap-up changes on external services:

    1. Push the changes to upstream repository and its mirror::

         hg push
         hg push bitbucket

    2. Go to `Read the Docs administrative pages
       <https://readthedocs.org/projects/django-conntrackt/>`_, and
       add the build for new version, retiring any unsupported
       versions along the way.

    3. Mark issue as resolved in the issue tracker.

    4. Release the version via release center in the issue tracker.

    5. Archive all other releases.
