# -*- coding: utf-8 -*-
"""TODO: doc module"""


import logging
from unittest import TestCase
from unittest import skip
from qatestlink.core.testlink_manager import TLManager
from qatestlink.core.models.tl_models import TProject
#from xml.etree.ElementTree import Element
#from qatestlink.core.TlConnectionBase import TlConnectionBase
#from qatestlink.core.xmls.XmlParserBase import XmlParserBase
#from qatestlink.core.objects.TlTestProject import TlTestProject
#from tests.config import Config
API_DEV_KEY = 'ae2f4839476bea169f7461d74b0ed0ac'


class TestModule(TestCase):
    """TODO: doc class"""

    @classmethod
    def setUpClass(cls):
        cls.testlink_manager = TLManager()

    def setUp(self):
        self.assertIsInstance(
            self.testlink_manager, TLManager)
        self.assertIsInstance(
            self.testlink_manager.log, logging.Logger)

    def test000_conn_ok_bysettings(self):
        """TODO: doc method"""
        self.assertTrue(
            self.testlink_manager.api_login())

    def test001_conn_ok_byparam(self):
        """TODO: doc method"""
        self.assertTrue(
            self.testlink_manager.api_login(
                dev_key=API_DEV_KEY))

    def test002_conn_ok_notdevkey(self):
        """TODO: doc method"""
        self.assertTrue(
            self.testlink_manager.api_login(
                dev_key=None))

    def test003_raises_conn_emptydevkey(self):
        """TODO: doc method"""
        self.assertFalse(
            self.testlink_manager.api_login(
                dev_key=''))

    def test004_get_tprojects(self):
        """TODO: doc method"""
        tprojects = self.testlink_manager.api_get_tprojects(
            dev_key=API_DEV_KEY)
        self.assertIsInstance(tprojects, list)
        self.assertGreater(len(tprojects), 0)
        self.assertIsInstance(tprojects[0], TProject)
        for tproject in tprojects:
            self.testlink_manager.log.debug(repr(tproject))
