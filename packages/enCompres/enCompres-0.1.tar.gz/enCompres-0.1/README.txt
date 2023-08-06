To create a password encrypted zip file in python.

This is a simple wrapper on top of Minizip wrapper in python.
(http://www.winimage.com/zLibDll/minizip.html)

This software uses zlib.
License: zlib/libpng License.

install zlib

    linux:
    $ sudo apt-get install zlib
    mac:
    $ sudo port install zlib

install enCompress

    $ pip install enCompress

----------------------------------------------------------------------------

Provides two functions.
==============================

enCompress.enCompress("/srcfile/path", "/distfile/file.xls", "cecid")

  Args:
  1. src file path (string)
  2. src file name (string)
  3. cecid (string) 

  Return value:
  - returns 0 on success and -1 on failures




==============================
