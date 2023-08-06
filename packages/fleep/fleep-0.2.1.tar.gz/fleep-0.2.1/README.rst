fleep
=====

File format identification library for Python

Getting Started
---------------

**fleep** is a library that identifies file format by file signature (also known as "magic number").

Installation
------------

You can install fleep using *pip*. Simply run in CLI:

::

    pip install fleep

Requirements
------------

-  Python >= 3.0

Example
-------

fleep has only one function **get()**. It takes two arguments:

-  *input* - path to the file or array of bytes
-  *output* - type of output values: extension or mime

There are some examples:

.. code:: python

    import fleep
    print(fleep.get(input="path_to_jpg_image", output="extension")) # prints ['jpg']

.. code:: python

    import fleep
    file = open("path_to_flac_file", "rb").read(1024)
    print(fleep.get(input=file, output="mime")) # prints ['audio/flac']

Supported formats
-----------------

There is a list of supported formats:

*Image:*

-  ai
-  bmp
-  gif
-  jpg
-  jp2
-  png
-  webp
-  ico
-  psd
-  eps
-  tiff

*Audio:*

-  aiff
-  aac
-  midi
-  mp3
-  m4a
-  oga
-  wav
-  wma
-  flac
-  mka

*Video:*

-  3g2
-  3gp
-  avi
-  flv
-  m4v
-  mkv
-  mov
-  mp4
-  swf
-  mpg
-  vob
-  wmv
-  asf
-  ogv
-  webm

*Document:*

-  odp
-  ods
-  odt
-  doc
-  pps
-  ppt
-  xls
-  docx
-  pptx
-  xlsx
-  pdf
-  rtf
-  epub

*Archive:*

-  7z
-  rar
-  tar.z
-  gz
-  zip
-  dmg
-  iso

*Executable:*

-  com
-  exe
-  jar

*Other:*

-  dll
-  sys
-  sqlite

License
-------

This project is licensed under the *MIT License*.

Contributing
------------

It would be nice to identify more formats. You can help us to deal with it!

Authors
-------

**Mykyta Paliienko** - `GitHub profile`_

.. _GitHub profile: https://github.com/floyernick