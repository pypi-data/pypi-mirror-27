# -*- coding: utf-8 -*-
"""TODO: doc module"""


import logging
from unittest import TestCase
from qatestlink.core.testlink_manager import TLManager
from qatestlink.core.exceptions.response_exception import ResponseException


API_DEV_KEY = 'ae2f4839476bea169f7461d74b0ed0ac'


class TestConnection(TestCase):
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

    def test_001_connok_bysettings(self):
        """TODO: doc method"""
        self.assertTrue(
            self.testlink_manager.api_login())

    def test_002_connok_byparam(self):
        """TODO: doc method"""
        self.assertTrue(
            self.testlink_manager.api_login(
                dev_key=API_DEV_KEY))

    def test_003_connok_notdevkey(self):
        """TODO: doc method"""
        self.assertTrue(
            self.testlink_manager.api_login(
                dev_key=None))


class TestConnectionRaises(TestCase):
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

    def test_001_raises_connemptydevkey(self):
        """TODO: doc method"""
        self.assertRaises(
            ResponseException,
            self.testlink_manager.api_login, dev_key='')
