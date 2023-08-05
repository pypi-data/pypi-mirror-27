================================================
devpi-web: web interface plugin for devpi-server
================================================

This plugin adds a web interface with search for `devpi-server`_.

.. _devpi-server: http://pypi.python.org/pypi/devpi-server


Installation
============

``devpi-web`` needs to be installed alongside ``devpi-server``.

You can install it with::

    pip install devpi-web

There is no configuration needed as ``devpi-server`` will automatically discover the plugin through calling hooks using the setuptools entry points mechanism.


=========
Changelog
=========



.. towncrier release notes start

3.2.1 (2017-11-23)
==================

No significant changes.


3.2.1rc1 (2017-09-08)
=====================

Bug Fixes
---------

- make search results compatible with pip showing INSTALLED/LATEST info.

- fix server error by returning 404 when a toxresult can't be found.


3.2.0 (2017-04-23)
==================

- version.pt: add "No releases" when there are none.

- project.pt: add "Documentation" column with link to documentation per version.


3.1.1 (2016-07-15)
==================

- removed unnecessary fetching of mirror data during indexing.


3.1.0 (2016-04-22)
==================

- use readme-renderer like PyPI does.

- if rendering the description causes errors, they are appended at the end.

- When creating the preview snippet for search results on documentation and the
  extracted doc files can't be accessed, then the preview will contain error
  information instead of raising an internal server error. See issue324

- fix issue335: The documentation wasn't linked for projects with
  non-normalized names.

- fix issue324: The project name wasn't correctly normalized when trying to
  access unpacked documentation in some code paths.

- all generated URLs in devpi-web are now normalized and don't go through a
  redirect anymore.

- added some internal infos to view data for use in theme templates. Any view
  data starting with an underscore is internal and may change between releases
  without notice. see issue319



