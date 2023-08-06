# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""TODO: doc module"""


import logging
from unittest import TestCase
from unittest import skipIf
from qatestlink.core.xmls.error_handler import ResponseException
from qatestlink.core.testlink_manager import TLManager
from qatestlink.core.models.tl_models import TProject
from qatestlink.core.models.tl_models import TPlan
from qatestlink.core.models.tl_models import TSuite
from qatestlink.core.models.tl_models import TPlatform


API_DEV_KEY = 'ae2f4839476bea169f7461d74b0ed0ac'
SKIP = False
CONFIG = {
    "tproject_name": "qacode",
    "tproject_id" : 11,
    "tplan_name" : "v0.3.8",
    "tplan_id" : 12
}


class TestMethods(TestCase):
    """TODO: doc class"""

    @classmethod
    def setUpClass(cls):
        """TODO: doc method"""
        cls.testlink_manager = TLManager()

    def setUp(self):
        """TODO: doc method"""
        self.assertIsInstance(
            self.testlink_manager, TLManager)
        self.assertIsInstance(
            self.testlink_manager.log, logging.Logger)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_001_method_tprojects(self):
        """TODO: doc method"""
        tprojects = self.testlink_manager.api_tprojects(
            dev_key=API_DEV_KEY)
        self.assertIsInstance(tprojects, list)
        self.assertGreater(len(tprojects), 0)
        for tproject in tprojects:
            self.testlink_manager.log.debug(repr(tproject))
            self.assertIsInstance(tproject, TProject)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_002_method_tproject(self):
        """TODO: doc method"""
        tproject = self.testlink_manager.api_tproject(CONFIG['tproject_name'])
        self.assertIsInstance(tproject, TProject)
        self.assertEquals(tproject.name, CONFIG['tproject_name'])

    @skipIf(SKIP, 'Test SKIPPED')
    def test_003_method_tproject_tplans(self):
        """TODO: doc method"""
        tplans = self.testlink_manager.api_tproject_tplans(CONFIG['tproject_id'])
        self.assertIsInstance(tplans, list)
        self.assertGreater(len(tplans), 0)
        for tplan in tplans:
            self.testlink_manager.log.debug(repr(tplan))
            self.assertIsInstance(tplan, TPlan)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_004_method_tproject_tsuites_first_level(self):
        """TODO: doc method"""
        tsuites = self.testlink_manager.api_tproject_tsuites_first_level(
            CONFIG['tproject_id'])
        self.assertIsInstance(tsuites, list)
        self.assertGreater(len(tsuites), 0)
        for tsuite in tsuites:
            self.testlink_manager.log.debug(repr(tsuite))
            self.assertIsInstance(tsuite, TSuite)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_005_method_tplan(self):
        """TODO: doc method"""
        tplan = self.testlink_manager.api_tplan(
            CONFIG['tproject_name'], CONFIG['tplan_name'])
        self.assertIsInstance(tplan, TPlan)
        self.assertEquals(tplan.name, CONFIG['tplan_name'])

    @skipIf(SKIP, 'Test SKIPPED')
    def test_006_method_tplan_platforms(self):
        """TODO: doc method"""
        platforms = self.testlink_manager.api_tplan_platforms(
            CONFIG['tplan_id'])
        self.assertIsInstance(platforms, list)
        self.assertGreater(len(platforms), 0)
        for platform in platforms:
            self.testlink_manager.log.debug(repr(platform))
            self.assertIsInstance(platform, TPlatform)


class TestMethodsRaises(TestCase):
    """TODO: doc class"""

    @classmethod
    def setUpClass(cls):
        """TODO: doc method"""
        cls.testlink_manager = TLManager()

    def setUp(self):
        """TODO: doc method"""
        self.assertIsInstance(
            self.testlink_manager, TLManager)
        self.assertIsInstance(
            self.testlink_manager.log, logging.Logger)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_001_raises_tproject_notname(self):
        """TODO: doc method"""
        self.assertRaises(
            Exception, self.testlink_manager.api_tproject)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_002_raises_tproject_emptyname(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_tproject,
            '')

    @skipIf(SKIP, 'Test SKIPPED')
    def test_003_raises_tproject_tplans_notid(self):
        """TODO: doc method"""
        self.assertRaises(
            Exception, self.testlink_manager.api_tproject_tplans)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_004_raises_tproject_tplans_notfoundid(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_tproject_tplans,
            -1)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_005_raises_tproject_tsuites_first_level_notid(self):
        """TODO: doc method"""
        self.assertRaises(
            Exception, self.testlink_manager.api_tproject_tsuites_first_level)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_006_raises_tproject_tsuites_first_level_notfoundid(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_tproject_tsuites_first_level,
            -1)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_007_raises_tplan_notname(self):
        """TODO: doc method"""
        self.assertRaises(
            Exception, self.testlink_manager.api_tplan)

    @skipIf(True, 'Test SKIPPED, waiting for issue https://github.com/viglesiasce/testlink/issues/7')
    def test_008_raises_tplan_emptytprojectname(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_tplan,
            '',
            CONFIG['tplan_name'])

    @skipIf(True, 'Test SKIPPED, waiting for issue https://github.com/viglesiasce/testlink/issues/7')
    def test_009_raises_tplan_emptytplanname(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_tplan,
            CONFIG['tproject_name'],
            '')

    @skipIf(True, 'Test SKIPPED, waiting for issue https://github.com/viglesiasce/testlink/issues/7')
    def test_010_raises_tplan_emptytnames(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_tplan,
            '', '')

    @skipIf(SKIP, 'Test SKIPPED')
    def test_011_raises_tplan_platforms_notname(self):
        """TODO: doc method"""
        self.assertRaises(
            Exception, self.testlink_manager.api_tproject)

    @skipIf(SKIP, 'Test SKIPPED')
    def test_012_raises_tplan_platforms_emptyname(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_tproject,
            '')
