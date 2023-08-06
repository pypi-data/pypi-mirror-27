
QA Testlink
===========

*qatestlink XMLRPC manager for Testlink*



.. image:: https://img.shields.io/github/issues/netzulo/qatestlink.svg
  :alt: Issues on Github
  :target: https://github.com/netzulo/qatestlink/issues

.. image:: https://img.shields.io/github/issues-pr/netzulo/qatestlink.svg
  :alt: Pull Request opened on Github
  :target: https://github.com/netzulo/qatestlink/issues

.. image:: https://img.shields.io/github/release/netzulo/qatestlink.svg
  :alt: Release version on Github
  :target: https://github.com/netzulo/qatestlink/releases/latest

.. image:: https://img.shields.io/github/release-date/netzulo/qatestlink.svg
  :alt: Release date on Github
  :target: https://github.com/netzulo/qatestlink/releases/latest

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


TOX environments
****************

+---------------------+--------------------------------+
| Env name            | Env description                |
+=====================+================================+
| py27,py34,py35,py36 | Python supported versions      |
+---------------------+--------------------------------+
| docs                | Generate doc HTML in /docs     |
+---------------------+--------------------------------+
| flake8              | Exec linter in qalab/ tests/   |
+---------------------+--------------------------------+
| coverage            | Generate XML and HTML reports  |
+---------------------+--------------------------------+


Usage ( *XMLRPC* )
**********************************

+ 1. Create JSON configuration ( runtime or read from file, *read config section* )
+ 2. Instance **testlink_manager** object ``testlink_manager = TLManager(settings=my_json_config)``
+ 3. Use some *method name with prefix* '**api_**'

**api_login**
+++++++++++++

* **XMLRPC**: *call to method named* '*tl.checkDevKey*'
* **Description** : check if dev_key it's valid

**api_tprojects** 
+++++++++++++++++

* **XMLRPC**: *call to method named* '*tl.getProjects*'
* **Description** : get all test projects


**api_tproject**
+++++++++++++++++

* **XMLRPC**: *call to method named* '*tl.getTestProjectByName*'
* **Description** : get one test project filtered by name

**api_tproject_tplans** 
+++++++++++++++++++++++

* **XMLRPC**: *call to method named* '*tl.getProjectTestPlans*'
* **Description** : get all test plans for one test project

**api_tproject_tsuites_first_level**
++++++++++++++++++++++++++++++++++++

* **XMLRPC**: *call to method named* '*tl.getFirstLevelTestSuitesForTestProject*'
* **Description** : get all test suites on first level for one test project

**api_tplan**
+++++++++++++

* **XMLRPC**: *call to method named* '*tl.getTestPlanByName*'
* **Description** : get one test plan filtered by project and plan names

**api_tplan_platforms**
+++++++++++++++++++++++

* **XMLRPC**: *call to method named* '*tl.getTestPlanPlatforms*'
* **Description** : get one test plan filtered by project and plan names
