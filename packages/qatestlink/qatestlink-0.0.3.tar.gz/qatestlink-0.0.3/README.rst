qatestlink
==========

*qatestlink XMLRPC manager for Testlink*



.. image:: https://img.shields.io/github/downloads/netzulo/qatestlink/total.svg
  :alt: Downloads on Github
  :target: https://img.shields.io/github/downloads/netzulo/qatestlink/total.svg
.. image:: https://img.shields.io/pypi/dd/qatestlink.svg
  :alt: Downloads on Pypi
  :target: https://img.shields.io/pypi/dd/qatestlink.svg
.. image:: https://img.shields.io/github/release/netzulo/qatestlink.svg
  :alt: GitHub release
  :target: https://img.shields.io/github/release/netzulo/qatestlink.svg

+------------------------+-------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+
|  Branch                |  Linux Deploy                                                           |  Windows Deploy                                                                                  |
+========================+=========================================================================+==================================================================================================+
|  master                |  .. image:: https://travis-ci.org/netzulo/qatestlink.svg?branch=master  |  .. image:: https://ci.appveyor.com/api/projects/status/7low4kw7qa6a5vem/branch/master?svg=true  |
+------------------------+-------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------+


Python tested versions
----------------------

+  **3.6**
+  **3.5**
+  **3.4**
+  **3.3** (*not supported*)
+  **3.2** (*not supported*)
+  **2.7**


Code Metrics by sonarqube
----------------------------

.. image:: http://qalab.tk:82/api/badges/gate?key=qatestlink
  :alt: Quality Gate
  :target: http://qalab.tk:82/api/badges/gate?key=qatestlink
.. image:: http://qalab.tk:82/api/badges/measure?key=qatestlink&metric=lines
  :alt: Lines
  :target: http://qalab.tk:82/api/badges/gate?key=qatestlink
.. image:: http://qalab.tk:82/api/badges/measure?key=qatestlink&metric=bugs
  :alt: Bugs
  :target: http://qalab.tk:82/api/badges/gate?key=qatestlink
.. image:: http://qalab.tk:82/api/badges/measure?key=qatestlink&metric=vulnerabilities
  :alt: Vulnerabilities
  :target: http://qalab.tk:82/api/badges/gate?key=qatestlink
.. image:: http://qalab.tk:82/api/badges/measure?key=qatestlink&metric=code_smells
  :alt: Code Smells
  :target: http://qalab.tk:82/api/badges/gate?key=qatestlink
.. image:: http://qalab.tk:82/api/badges/measure?key=qatestlink&metric=sqale_debt_ratio
  :alt: Debt ratio
  :target: http://qalab.tk:82/api/badges/gate?key=qatestlink
.. image:: http://qalab.tk:82/api/badges/measure?key=qatestlink&metric=comment_lines_density
  :alt: Comments
  :target: http://qalab.tk:82/api/badges/gate?key=qatestlink


PIP install
-----------

``pip install qatestlink``

SETUP.py install
----------------

``python setup.py install``


Configuration File
------------------

.. highlight:: json
.. code-block:: json
   :linenos:

::

    {
      "connection":{
        "is_https": false,
        "host": "qalab.tk",
        "port": 86
      },
      "dev_key": "ae2f4839476bea169f7461d74b0ed0ac",
      "log_level":"DEBUG"
    }


Tests
-----

*You will need real testlink app running before you can just execute on command line*

``python setup.py test``
