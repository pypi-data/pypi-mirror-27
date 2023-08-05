+----------------------+-------------+------------+-----------------+----------------+
| CI Builds            | fdroidserve | buildserve | fdroid build    | publishing     |
|                      | r           | r          | --all           | tools          |
+======================+=============+============+=================+================+
| Debian               | |fdroidserv | |buildserv | |fdroid build   | |fdroid build  |
|                      | er          | er         | all status|     | all status|    |
|                      | status on   | status|    |                 |                |
|                      | Debian|     |            |                 |                |
+----------------------+-------------+------------+-----------------+----------------+
| macOS & Ubuntu/LTS   | |fdroidserv |            |                 |                |
|                      | er          |            |                 |                |
|                      | status on   |            |                 |                |
|                      | macOS &     |            |                 |                |
|                      | Ubuntu/LTS| |            |                 |                |
+----------------------+-------------+------------+-----------------+----------------+

F-Droid Server
==============

Server for `F-Droid <https://f-droid.org>`__, the Free Software
repository system for Android.

The F-Droid server tools provide various scripts and tools that are used
to maintain the main `F-Droid application
repository <https://f-droid.org/packages>`__. You can use these same
tools to create your own additional or alternative repository for
publishing, or to assist in creating, testing and submitting metadata to
the main repository.

For documentation, please see https://f-droid.org/docs/, or you can find
the source for the documentation in
`fdroid/fdroid-website <https://gitlab.com/fdroid/fdroid-website>`__.

What is F-Droid?
~~~~~~~~~~~~~~~~

F-Droid is an installable catalogue of FOSS (Free and Open Source
Software) applications for the Android platform. The client makes it
easy to browse, install, and keep track of updates on your device.

Installing
~~~~~~~~~~

There are many was to install *fdroidserver*, they are documented on the
website:
https://f-droid.org/docs/Installing\_the\_Server\_and\_Repo\_Tools

All sorts of other documentation lives there as well.

Drozer Scanner
~~~~~~~~~~~~~~

There is a new feature under development that can scan any APK in a
repo, or any build, using Drozer. Drozer is a dynamic exploit scanner,
it runs an app in the emulator and runs known exploits on it.

This setup requires specific versions of two Python modules: *docker-py*
1.9.0 and *requests* older than 2.11. Other versions might cause the
docker-py connection to break with the containers. Newer versions of
docker-py might have this fixed already.

For Debian based distributions:

::

    apt-get install libffi-dev libssl-dev python-docker

Translation
-----------

Everything can be translated. See `Translation and
Localization <https://f-droid.org/docs/Translation_and_Localization>`__
for more info. |translation status|

.. |fdroidserver status on Debian| image:: https://gitlab.com/fdroid/fdroidserver/badges/master/build.svg
   :target: https://gitlab.com/fdroid/fdroidserver/builds
.. |buildserver status| image:: https://jenkins.debian.net/job/reproducible_setup_fdroid_build_environment/badge/icon
   :target: https://jenkins.debian.net/job/reproducible_setup_fdroid_build_environment
.. |fdroid build all status| image:: https://jenkins.debian.net/job/reproducible_fdroid_build_apps/badge/icon
   :target: https://jenkins.debian.net/job/reproducible_fdroid_build_apps/
.. |fdroid build all status| image:: https://jenkins.debian.net/job/reproducible_fdroid_test/badge/icon
   :target: https://jenkins.debian.net/job/reproducible_fdroid_test/
.. |fdroidserver status on macOS & Ubuntu/LTS| image:: https://travis-ci.org/f-droid/fdroidserver.svg?branch=master
   :target: https://travis-ci.org/f-droid/fdroidserver
.. |translation status| image:: https://hosted.weblate.org/widgets/f-droid/-/fdroidserver/multi-auto.svg
   :target: https://hosted.weblate.org/engage/f-droid/?utm_source=widget
