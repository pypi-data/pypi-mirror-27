# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Testlink Managers"""


from qatestlink.core.utils.Utils import settings as settings_func
from qatestlink.core.utils.logger_manager import LoggerManager
from qatestlink.core.connections.connection_base import ConnectionBase
from qatestlink.core.xmls.xmlrpc_manager import XMLRPCManager



PATH_CONFIG = 'qatestlink/configs/settings.json'

class TLManager(object):
    """
    This class allows to send, handle and interpretate reponses
     to/from testlink api XMLRPC
    """

    _settings_path = None
    _settings = None
    _logger_manager = None
    _xml_manager = None
    _conn = None

    log = None

    def __init__(self, file_path=None, file_name=None, settings=None):
        """
        This instance allow to handle requests+reponses to/from XMLRPC
        just need settings_path and settings dict loaded to works

        :Args:
            settings_path: Path for search JSON
                file with settings values
            settings: Load settings at default path,
                'qatestlink/configs/settings.json'
        """
        if settings is None:
            if file_path is None or file_name is None:
                settings = settings_func()
            else:
                settings = settings_func(
                    file_path=file_path,
                    file_name=file_name)
        self._settings = settings
        self._logger_manager = LoggerManager(
            self._settings.get('log_level'))
        self.log = self._logger_manager.log
        self._xml_manager = XMLRPCManager(self.log)
        # generate url using settings
        conn = self._settings.get('connection')
        self._conn = ConnectionBase(
            self.log,
            host=conn.get('host'),
            port=conn.get('port'),
            is_https=conn.get('is_https'))

    def api_login(self, dev_key=None):
        """Call to method named 'checkDevKey' for testlink XMLRPC"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_check_dev_key(dev_key)
        res = self._conn.post(self._xml_manager.headers, req_data)
        self._xml_manager.parse_errors(res.text)
        res_xml = self._xml_manager.res_check_dev_key(
            res.status_code, res.text)
        node_boolean = self._xml_manager.handler.find_node(
            'boolean', xml_str=res_xml)
        if node_boolean is None:
            return False
        return bool(node_boolean.text)

    def api_tprojects(self, dev_key=None):
        """Call to method named 'tl.getProjects'"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_tprojects(dev_key)
        res = self._conn.post(self._xml_manager.headers, req_data)
        self._xml_manager.parse_errors(res.text)
        res_as_models = self._xml_manager.res_tprojects(
            res.status_code, res.text, as_models=True)
        # TODO: filter by name and/or value
        return res_as_models

    def api_tproject(self, tproject_name, dev_key=None):
        """Call to method named 'tl.getTestProjectByName'"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_tproject_by_name(
            dev_key, tproject_name)
        res = self._conn.post(self._xml_manager.headers, req_data)
        self._xml_manager.parse_errors(res.text)
        res_as_model = self._xml_manager.res_tproject_by_name(
            res.status_code, res.text, as_model=True)
        return res_as_model

    def api_tproject_tplans(self, tproject_id, dev_key=None):
        """Call to method named 'tl.getProjectTestPlans'"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_tproject_tplans(
            dev_key, tproject_id)
        res = self._conn.post(self._xml_manager.headers, req_data)
        self._xml_manager.parse_errors(res.text)
        res_as_models = self._xml_manager.res_tproject_tplans(
            res.status_code, res.text, as_models=True)
        return res_as_models

    def api_tproject_tsuites_first_level(self, tproject_id, dev_key=None):
        """Call to method named 'tl.getFirstLevelTestSuitesForTestProject'"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_tproject_tsuites_first_level(
            dev_key, tproject_id)
        res = self._conn.post(self._xml_manager.headers, req_data)
        self._xml_manager.parse_errors(res.text)
        res_as_models = self._xml_manager.res_tproject_tsuites_first_level(
            res.status_code, res.text, as_models=True)
        return res_as_models

    def api_tplan(self, tproject_name, tplan_name, dev_key=None):
        """Call to method named 'tl.getTestPlanByName'"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_tplan_by_name(
            dev_key, tproject_name, tplan_name)
        res = self._conn.post(self._xml_manager.headers, req_data)
        self._xml_manager.parse_errors(res.text)
        res_as_model = self._xml_manager.res_tplan_by_name(
            res.status_code, res.text, as_model=True)
        return res_as_model

    def api_tplan_platforms(self, tplan_id, dev_key=None):
        """Call to method named 'tl.getTestPlanPlatforms'"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_tplan_platforms(
            dev_key, tplan_id)
        res = self._conn.post(self._xml_manager.headers, req_data)
        self._xml_manager.parse_errors(res.text)
        res_as_models = self._xml_manager.res_tplan_platforms(
            res.status_code, res.text, as_models=True)
        return res_as_models
