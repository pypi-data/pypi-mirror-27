
TFATool: Toshiba FlashAir Tool
==============================

This package provides easy access to
Toshiba's FlashAir wireless SD card. As a library,
a simple abstraction of the FlashAir API is provided. As a set of
scripts, `tfatool` the user is given a way of synchronizing/mirroring
files and configuring the device from the command line.

Package contents at a glance
============================

* ``flashair-util``: a command line tool for mirroring and listing files on FlashAir
* ``flashair-config``: a command line tool for configuring FlashAir
* ``tfatool.command``: abstraction of FlashAir's `command.cgi <https://flashair-developers.com/en/documents/api/commandcgi/>`_
* ``tfatool.upload``: abstraction of FlashAir's `upload.cgi  <https://flashair-developers.com/en/documents/api/uploadcgi/>`_
* ``tfatool.config``: abstraction of FlashAir's `config.cgi <https://flashair-developers.com/en/documents/api/configcgi/>`_
* ``tfatool.sync``: functions for synchronizing local dirs with remote FlashAir dirs

Command line usage at a glance
==============================

1. Monitor FlashAir for new JPEGs, download to ~/Photos

   ``flashair-util -s -d /home/tad/Photos --only-jpg``

2. Monitor working dir for new files, upload to FlashAir

   ``flashair-util -s -y up``

3. Monitor a local and remote dir for new files, sync them

   ``flashair-util -s -y both``

4. Sync down the 10 most recent to a local dir, then quit

   ``flashair-util -S time -d images/new/``

5. Sync up all files created in 1999 and afterwards

   ``flashair-util -S all -t 1999``

6. Sync down files created between Jan 23rd and Jan 26th

   ``flashair-util -S all -t 1-23 -T 01/26``

7. Sync files (up AND down) created this afternoon

   ``flashair-util -S all -t 12:00 -T 16:00 -y  both``

8. Sync files up created after a very specific date/time

   ``flashair-util -S all -t '2016-1-25 11:38:22'``

9. Sync (up and down) 5 most recent files of a certain name

   ``flashair-util -S time -k 'IMG-08.+\.raw' -y both``

10. List files on FlashAir created after a certain time

    ``flashair-util -l -t '1-21-2016 8:30:11'``

11. Change FlashAir network SSID

    ``flashair-config --wifi-ssid myflashairnetwork``

12. Show FlashAir network password & firmware version

    ``flashair-config --show-wifi-key --show-fw-version``

More
====

See https://github.com/TadLeonard/tfatool for complete documentation.


