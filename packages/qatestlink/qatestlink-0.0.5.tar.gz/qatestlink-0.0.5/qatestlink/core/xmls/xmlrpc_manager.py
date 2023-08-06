# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""XMLRPC managers"""

from qatestlink.core.xmls.route_type import RouteType
from qatestlink.core.xmls.error_handler import ErrorHandler
from qatestlink.core.xmls.request_handler import RequestHandler
from qatestlink.core.xmls.response_handler import ResponseHandler
from qatestlink.core.xmls.base_handler import BaseHandler
from qatestlink.core.models.tl_models import TProject
from qatestlink.core.models.tl_models import TPlan
from qatestlink.core.models.tl_models import TSuite
from qatestlink.core.models.tl_models import TPlatform



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
        self._error_handler = ErrorHandler(self.log)
        self.headers = {'Content-Type': 'application/xml'}
        self.handler = BaseHandler(self.log)

    def parse_errors(self, xml_str):
        """Raise an exception if response have error structure"""
        #TODO: make enum and custom exception for each exception number
        self._error_handler.get_response_error(xml_str)

    def req_check_dev_key(self, dev_key):
        """
        :return:
            string xml object ready to use on API call
        """
        req = self._request_handler.create(
            RouteType.TLINK_CHECK_DEV_KEY)
        return self._request_handler.create_param(
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

    def req_tprojects(self, dev_key):
        """
        Obtains all test projects created on remote
         testlink database,
         TODO: can filter with any property+value combination

        :return:
            List of TProject objects containing all database
             data loaded
        """
        req = self._request_handler.create(
            RouteType.TPROJECTS)
        return self._request_handler.create_param(
            req, 'struct', 'devKey', dev_key)

    def res_tprojects(self, status_code, res_str, as_models=True):
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
        res_members_list = self._response_handler.get_response_members(
            xml_str=res)
        tprojects = list()
        for res_members in res_members_list:
            tproject = TProject(res_members)
            tprojects.append(tproject)
        return tprojects


    def req_tproject_by_name(self, dev_key, tproject_name):
        """
        Obtains all test projects created on remote
         testlink database, can filter by name

        :return:
            TProject object containing all database
             data loaded
        """
        if tproject_name is None:
            raise Exception("Can't call XMLRPC without param, tproject_name")
        req = self._request_handler.create(
            RouteType.TPROJECT_BY_NAME)
        req = self._request_handler.create_param(
            req, 'struct', 'devKey', dev_key)
        req = self._request_handler.add_param(
            req, 'testprojectname', tproject_name)
        return req

    def res_tproject_by_name(self, status_code, res_str, as_model=True):
        """
        Parse and validate response for method
         named 'tl.getTestProjectByName', by default response
         TProject object, can response xml string too
        :return:
            if as_models is True
                object instanced with Model classes
            if as_models is False
                string xml object ready to
                 parse/write/find/add Elements on it
        """
        if status_code != 200:
            raise Exception(
                "status_code invalid: code={}".format(
                    status_code))
        res = self._response_handler.create(
            RouteType.TPROJECT_BY_NAME, res_str)
        if not as_model:
            return res
        res_members_list = self._response_handler.get_response_struct_members(
            xml_str=res)
        return TProject(res_members_list)


    def req_tproject_tplans(self, dev_key, tproject_id):
        """
        Obtains all test plans asigned to test project
         created on remote testlink database,
         can filter by project id

        :return:
            List of TPlan objects containing all database
             data loaded
        """
        if tproject_id is None:
            raise Exception("Can't call XMLRPC without param, tproject_id")
        req = self._request_handler.create(
            RouteType.TPROJECT_TEST_PLANS)
        req = self._request_handler.create_param(
            req, 'struct', 'devKey', dev_key)
        req = self._request_handler.add_param(
            req, 'testprojectid', tproject_id)
        return req


    def res_tproject_tplans(self, status_code, res_str, as_models=True):
        """
        Parse and validate response for method
         named 'tl.getProjectTestPlans', by default response list
         of TPlan objects, can response xml string too
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
            RouteType.TPROJECT_TEST_PLANS, res_str)
        if not as_models:
            return res
        res_members_list = self._response_handler.get_response_members(
            xml_str=res)
        tplans = list()
        for res_members in res_members_list:
            tplan = TPlan(res_members)
            tplans.append(tplan)
        return tplans

    def req_tproject_tsuites_first_level(self, dev_key, tproject_id):
        """
        Obtains all test suites of first level into test project
         created on remote testlink database,
         can filter by project id

        :return:
            List of TSuite objects containing all database
             data loaded
        """
        if tproject_id is None:
            raise Exception("Can't call XMLRPC without param, tproject_id")
        req = self._request_handler.create(
            RouteType.TPROJECT_TSUITES_FIRST_LEVEL)
        req = self._request_handler.create_param(
            req, 'struct', 'devKey', dev_key)
        req = self._request_handler.add_param(
            req, 'testprojectid', tproject_id)
        return req


    def res_tproject_tsuites_first_level(self, status_code, res_str, as_models=True):
        """
        Parse and validate response for method
         named 'tl.getFirstLevelTestSuitesForTestProject', by default
         response list of TSuite objects, can response xml string too
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
            RouteType.TPROJECT_TSUITES_FIRST_LEVEL, res_str)
        if not as_models:
            return res
        res_members_list = self._response_handler.get_response_members(
            xml_str=res)
        tsuites = list()
        for res_members in res_members_list:
            tsuite = TSuite(res_members)
            tsuites.append(tsuite)
        return tsuites

    def req_tplan_by_name(self, dev_key, tproject_name, tplan_name):
        """
        Obtains all test projects created on remote
         testlink database, can filter by name

        :return:
            TProject object containing all database
             data loaded
        """
        if tproject_name is None:
            raise Exception("Can't call XMLRPC without param, tproject_name")
        if tplan_name is None:
            raise Exception("Can't call XMLRPC without param, tplan_name")
        req = self._request_handler.create(
            RouteType.TPLAN_BY_NAME)
        req = self._request_handler.create_param(
            req, 'struct', 'devKey', dev_key)
        req = self._request_handler.add_param(
            req, 'testprojectname', tproject_name)
        req = self._request_handler.add_param(
            req, 'testplanname', tplan_name)
        return req

    def res_tplan_by_name(self, status_code, res_str, as_model=True):
        """
        Parse and validate response for method
         named 'tl.getTestProjectByName', by default response
         TProject object, can response xml string too
        :return:
            if as_models is True
                object instanced with Model classes
            if as_models is False
                string xml object ready to
                 parse/write/find/add Elements on it
        """
        if status_code != 200:
            raise Exception(
                "status_code invalid: code={}".format(
                    status_code))
        res = self._response_handler.create(
            RouteType.TPLAN_BY_NAME, res_str)
        if not as_model:
            return res
        res_members_list = self._response_handler.get_response_struct_members(
            xml_str=res)
        return TPlan(res_members_list)

    def req_tplan_platforms(self, dev_key, tplan_id):
        """
        Obtains all platforms asigned to test plan
         created on remote testlink database,
         can filter by test plan name

        :return:
            List of TPlan objects containing all database
             data loaded
        """
        if tplan_id is None:
            raise Exception("Can't call XMLRPC without param, tplan_id")
        req = self._request_handler.create(
            RouteType.TPLAN_PLATFORMS)
        req = self._request_handler.create_param(
            req, 'struct', 'devKey', dev_key)
        req = self._request_handler.add_param(
            req, 'testplanid', tplan_id)
        return req

    def res_tplan_platforms(self, status_code, res_str, as_models=True):
        """
        Parse and validate response for method
         named 'tl.getTestPlanPlatforms', by default response list
         of TPlatform objects, can response xml string too
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
            RouteType.TPLAN_PLATFORMS, res_str)
        if not as_models:
            return res
        res_members_list = self._response_handler.get_response_members(
            xml_str=res)
        tplatforms = list()
        for res_members in res_members_list:
            tplatform = TPlatform(res_members)
            tplatforms.append(tplatform)
        return tplatforms
