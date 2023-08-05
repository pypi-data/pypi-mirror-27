# -*- coding: utf-8 -*-
"""Testlink Managers"""


import json
import logging
import requests
from qatestlink.core.utils.logger_manager import LoggerManager
from qatestlink.core.connections.connection_base import ConnectionBase
from qatestlink.core.utils.Utils import read_file
from qatestlink.core.xmls.route_type import RouteType
from qatestlink.core.xmls.request_handler import RequestHandler
from qatestlink.core.xmls.response_handler import ResponseHandler
from qatestlink.core.xmls.base_handler import BaseHandler
from qatestlink.core.models.tl_models import TProject


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

    def __init__(self, settings_path=None, settings=None):
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
            settings = self.get_settings(json_path=settings_path)
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

    def get_settings(self, json_path=None):
        """
        Get default settings path or search on param path
         to load as a dict and return it
        """
        json_path_selected = PATH_CONFIG
        if json_path is not None:
            json_path_selected = json_path
        return read_file(file_path=json_path_selected, is_json=True)

    def api_login(self, dev_key=None):
        """Call to method named 'checkDevKey' for testlink XMLRPC"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_check_dev_key(dev_key)
        res = self._conn.post(self._xml_manager.headers, req_data)
        res_xml = self._xml_manager.res_check_dev_key(
            res.status_code, res.text)
        node_boolean = self._xml_manager.handler.find_node(
            'boolean', xml_str=res_xml)
        if node_boolean is None:
            return False
        return bool(node_boolean.text)

    def api_get_tprojects(self, dev_key=None):
        """Call to method naed ''"""
        if dev_key is None:
            dev_key = self._settings.get('dev_key')
        req_data = self._xml_manager.req_get_tprojects(dev_key)
        res = self._conn.post(self._xml_manager.headers, req_data)
        res_as_models = self._xml_manager.res_get_tprojects(
            res.status_code, res.text, as_models=True)
        # TODO: filter by name and/or value
        return res_as_models


class XMLRPCManager(object):
    """
    Manage all XMLRPCManager requests,
     responses and handle errors. This class
     store all official methods names used
     on original XMLRPC php class
    """
    _request_handler = None
    _response_handler = None
    _error_handler = None

    log = None
    headers = None
    handler = None

    def __init__(self, log):
        self.log = log
        self._request_handler = RequestHandler(self.log)
        self._response_handler = ResponseHandler(self.log)
        self._error_handler = None
        self.headers = {'Content-Type': 'application/xml'}
        self.handler = BaseHandler(self.log)

    def req_check_dev_key(self, dev_key):
        """
        :return:
            string xml object ready to use on API call
        """
        req = self._request_handler.create(
            RouteType.TLINK_CHECK_DEV_KEY)
        return self._request_handler.add_param(
            req, 'struct', 'devKey', dev_key)

    def res_check_dev_key(self, status_code, res_str):
        """
        :return:
            string xml object ready to
             parse/write/find/add Elements on it
        """
        if status_code != 200:
            raise Exception(
                "status_code invalid: code={}".format(
                    status_code))
        return self._response_handler.create(
            RouteType.TLINK_CHECK_DEV_KEY, res_str)

    def req_get_tprojects(self, dev_key):
        """
        Obtains all test projects created on remote
         testlink database, can filter with any property+value
         combination

        :return:
            List of TProject objects containing all database
             data loaded
        """
        req = self._request_handler.create(
            RouteType.TPROJECTS)
        return self._request_handler.add_param(
            req, 'struct', 'devKey', dev_key)

    def res_get_tprojects(self, status_code, res_str, as_models=True):
        """
        Parse and validate response for method
         named 'tl.getProjects', by default response list
         of TProject objects, can response xml string too
        :return:
            if as_models is True
                list of objects instanced with
                 Model classes
            if as_models is False
                string xml object ready to
                 parse/write/find/add Elements on it
        """
        if status_code != 200:
            raise Exception(
                "status_code invalid: code={}".format(
                    status_code))
        res = self._response_handler.create(
            RouteType.TPROJECTS, res_str)
        if not as_models:
            return res
        # TODO: create objects and return them as list
        res_members_list = self._response_handler.get_response_members(
            xml_str=res)
        # TODO: build objects
        tprojects = list()
        for res_members in res_members_list:
            #TODO: all members by project
            tproject = TProject(res_members)            
            tprojects.append(tproject)
        return tprojects



