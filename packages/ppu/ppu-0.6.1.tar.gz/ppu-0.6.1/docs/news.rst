News
====

Version 0.6.1 (2017-12-15)
--------------------------

* Fix rm.py: do not ask to remove read-only files when -f is active.

Version 0.6.0 (2017-12-13)
--------------------------

* rm.py ask interactively to remove read-only files or directories.

* Add options -s --silent --quiet for cmp.py.

* Add option -f for rm.py.

* PyPy.

Version 0.5.0 (2017-07-09)
--------------------------

* Add option -r for rm.py.

* Use remove-old-files.py to cleanup pip cache.

Version 0.4.0 (2017-06-04)
--------------------------

* Add package 'ppu'.

* Add module ppu/find_executable.py.

* Add script which.py.

Version 0.3.2 (2017-05-01)
--------------------------

* Convert README to reST.

Version 0.3.1 (2017-04-30)
--------------------------

* Fix release: build scripts with '/usr/bin/env python'

Version 0.3.0 (2017-04-30)
--------------------------

* Move cmp.py, remove-old-files.py and rm.py to scripts directory.

* Release at PyPI.

Version 0.2.0 (2017-04-30)
--------------------------

* Add cmp.py and rm.py.

* Test at Travis and AppVeyor.

* Use subprocess.call() instead of os.system().

0.1.0 (2017-04-16)
------------------

* Remove empty directories.

* Add installation instructions.

0.0.1 (2017-04-16)
------------------

* Initial release.
