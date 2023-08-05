|PyPI version| |Build Status| |Coverage Status| |BCH compliance|

tika-app-python
===============

Overview
--------

tika-app-python is a wrapper for `Apache Tika
App <https://tika.apache.org/>`__.

Apache 2 Open Source License
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tika-app-python can be downloaded, used, and modified free of charge. It
is available under the Apache 2 license.

Authors
-------

Main Author
~~~~~~~~~~~

Fedele Mantuano (**Twitter**:
[@fedelemantuano](https://twitter.com/fedelemantuano))

Installation
------------

Clone repository

::

    git clone https://github.com/fedelemantuano/tika-app-python.git

and install tika-app-python with ``setup.py``:

::

    cd tika-app-python

    python setup.py install

or use ``pip``:

::

    pip install tika-app

Usage in a project
------------------

Import ``TikaApp`` class:

::

    from tikapp import TikaApp

    tika_client = TikaApp(file_jar="/opt/tika/tika-app-1.15.jar")

For get **content type**:

::

    tika_client.detect_content_type("your_file")

For detect **language**:

::

    tika_client.detect_language("your_file")

For detect **all metadata and content**:

::

    tika_client.extract_all_content("your_file")

For detect **only content**:

::

    tika_client.extract_only_content("your_file")

If you want to use payload in base64, you can use the same methods with
``payload`` argument:

::

    tika_client.detect_content_type(payload="base64_payload")
    tika_client.detect_language(payload="base64_payload")
    tika_client.extract_all_content(payload="base64_payload")
    tika_client.extract_only_content(payload="base64_payload")

Usage from command-line
-----------------------

If you installed tika-app-python with ``pip`` or ``setup.py`` you can
use it with command-line. To use tika-app-python you should submit the
Apache Tika app JAR. You can: - leave the default value:
``/opt/tika/tika-app-1.15.jar`` - set the enviroment value
``TIKA_APP_JAR`` - use ``--jar`` switch

The last one overwrite all the others.

These are all swithes:

::

    usage: tikapp [-h] (-f FILE | -p PAYLOAD) [-j JAR] [-d] [-t] [-l] [-a]
                       [-v]

    Wrapper for Apache Tika App.

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  File to submit (default: None)
      -p PAYLOAD, --payload PAYLOAD
                            Base64 payload to submit (default: None)
      -j JAR, --jar JAR     Apache Tika app JAR (default: None)
      -d, --detect          Detect document type (default: False)
      -t, --text            Output plain text content (default: False)
      -l, --language        Output only language (default: False)
      -a, --all             Output metadata and content from all embedded files
                            (default: False)
      -v, --version         show program's version number and exit

Example:

.. code:: shell

    $ tikapp -f example_file -a

Performance tests
-----------------

These are the results of performance tests in
`tests <https://github.com/fedelemantuano/tika-app-python/tree/develop/tests>`__
folder:

::

    (Python 2)
    tika_content_type()             0.704840 sec
    tika_detect_language()          1.592066 sec
    magic_content_type()            0.000215 sec
    tika_extract_all_content()      0.816366 sec
    tika_extract_only_content()     0.788667 sec

    (Python 3)
    tika_content_type()             0.698357 sec
    tika_detect_language()          1.593452 sec
    magic_content_type()            0.000226 sec
    tika_extract_all_content()      0.785915 sec
    tika_extract_only_content()     0.766517 sec

.. |PyPI version| image:: https://badge.fury.io/py/tika-app.svg
   :target: https://badge.fury.io/py/tika-app
.. |Build Status| image:: https://travis-ci.org/fedelemantuano/tika-app-python.svg?branch=master
   :target: https://travis-ci.org/fedelemantuano/tika-app-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/fedelemantuano/tika-app-python/badge.svg?branch=master
   :target: https://coveralls.io/github/fedelemantuano/tika-app-python?branch=master
.. |BCH compliance| image:: https://bettercodehub.com/edge/badge/fedelemantuano/tika-app-python?branch=develop
   :target: https://bettercodehub.com/
