=============================================================================
devpi-server: pypi server for caching and private indexes
=============================================================================

* `issue tracker <https://github.com/devpi/devpi/issues>`_, `repo
  <https://github.com/devpi/devpi>`_

* IRC: #devpi on freenode, `mailing list
  <https://mail.python.org/mm3/mailman3/lists/devpi-dev.python.org/>`_ 

* compatibility: {win,unix}-py{27,34,35,36,py}

consistent robust pypi-cache
============================

You can point ``pip or easy_install`` to the ``root/pypi/+simple/``
index, serving as a self-updating transparent cache for pypi-hosted
**and** external packages.  Cache-invalidation uses the latest and
greatest PyPI protocols.  The cache index continues to serve when
offline and will resume cache-updates once network is available.

user specific indexes
=====================

Each user (which can represent a person or a project, team) can have
multiple indexes and upload packages and docs via standard ``setup.py``
invocations command.  Users and indexes can be manipulated through a
RESTful HTTP API.

index inheritance
=================

Each index can be configured to merge in other indexes so that it serves
both its uploads and all releases from other index(es).  For example, an
index using ``root/pypi`` as a parent is a good place to test out a
release candidate before you push it to PyPI.

good defaults and easy deployment
=================================

Get started easily and create a permanent devpi-server deployment
including pre-configured templates for ``nginx`` and cron. 

separate tool for Packaging/Testing activities
==============================================

The complementary `devpi-client <http://pypi.python.org/devpi-client>`_ tool
helps to manage users, indexes, logins and typical setup.py-based upload and
installation workflows.

See http://doc.devpi.net for getting started and documentation.



=========
Changelog
=========



.. towncrier release notes start

4.3.1 (2017-11-23)
==================

Bug Fixes
---------

- fix +api on replica when master is down.


4.3.1rc1 (2017-09-08)
=====================

Bug Fixes
---------

- fix issue345: remove ``expires -1`` option in example nginx proxy config for
  devpi. When there are no ``Expires`` and ``Cache-Control`` headers, then pip
  does not cache the simple pages, the headers set by ``expires -1`` caused pip
  to cache for 5 minutes.

- fix issue402: the redirect to simple index didn't take X-Outside-Url into
  account.

- fix for url decoding issue with mirrors. When package filenames contain
  characters such as `!` or `+`, these get URL encoded to `%21` and `%2B` in
  the remote simple index. This fix ensures that in the filename saved to the
  disk cache these are decoded back to `!` or `+`.

- fix issue434: ``--status`` didn't work anymore. The background server
  functionality is now deprecated, see --gen-config to use a process manager
  from your OS.

- fix issue449: push to pypi broke again due to a changed reply.

- fix remote file url for mirrors not named "root/pypi" which provide file
  hashes.

- fix issue401: fix traceback and inaccessible index by ignoring removed bases.


4.3.0 (2017-04-23)
==================

- allow upload of documentation without first registering the project or
  uploading releases.

- add a new command line option ``--replica-max-retries``

  Under certain network conditions, it's possible for a connection from devpi
  to replicas (such as pypi) to be dropped, resulting in a 502 bad gateway
  being returned from devpi. When replica-max-retries is set to a number > 0,
  devpi will attempt to retry connections until the retry limit is reached.

- fix ``--import`` after ``--init`` option was added.

- fix import when the export contains a bases cycle.

- fix issue350: use absolute path to devpi-server when starting
  background process.

- fix issue392: setting user password from command line when password hash
  wasn't migrated yet failed.

- fix #381: indicate acceptable exit status for systemd.

- remove broken ``--bypass-cdn`` option.


4.2.1 (2016-12-22)
==================

- the new ``--init`` option now exits after done, so it can be used in
  automation scripts. When using with ``--start`` it still starts the
  background server immediately.


4.2.0 (2016-12-14)
==================

SECURITY NOTE:

Before devpi-server 4.2.0 passwords were hashed with a very weak algorithm.
It's strongly recommended to change any passwords created before 4.2.0
after upgrading! The password salt and hashes are exposed via the /+changelog
URL used for replication. If you use replication you should use client
side certificates or https with basic authentication to secure /+changelog.

UPGRADE NOTE:

Starting with devpi-server 4.2.0 the replication protocol is disabled by
default to prevent accidental information leaks, like password hashes. To
enable the replication protocol, you have to use ``--role master`` when
starting the master devpi-server instance.

- fix issue378: the replication protocol is now disabled by default.

- fix push to PyPI by skipping failing "register" step and adding additional
  fields in POST data on "file_upload".

- fix issue372: correctly set isolation_level for sqlite3 connections. This
  also fixes Python 3.6 compatibility.

- fix issue334: The event handler for the simple page cache failed when an
  index was deleted and a new replica tried to run the event hooks.

- fix issue314: Fetch external file on replica from original source if master
  is down.

- fix issue363: Replace weak password hashing with argon2 using passlib.
  Existing logins will be migrated on login.

- fix issue377: Add new ``--init`` option required to initialize a server
  directory. This prevents accidental use of wrong or empty ``--serverdir``.

- fix issue285: require waitress >= 1.0.1 to enable IPv6 support.



