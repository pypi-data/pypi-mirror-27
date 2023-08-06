# -*- coding: utf-8 -*-
# pylint: disable=too-many-locals
# pylint: disable=useless-super-delegation
"""TODO: doc module"""


from xml.etree.ElementTree import tostring as xml_to_str
from qatestlink.core.xmls.base_handler import BaseHandler
from qatestlink.core.exceptions.response_exception import ResponseException


class ErrorHandler(BaseHandler):
    """TODO: doc class"""

    def __init__(self, *args, **kwargs):
        """Instance handler"""
        super(ErrorHandler, self).__init__(*args, **kwargs)

    def create(self, route_type, xml_str):
        """Create response by router_type"""
        super(ErrorHandler, self).is_route_type(route_type)
        root = self.xml_parse(xml_str)
        return xml_to_str(root)

    def get_response_error(self, xml_str):
        """
        Allow to parse string XML object list response to
         ResponseMember object list
        :Args:
            xml_str: must be XML format string
             <param>
               <value>
                 <array>
                   <data>
                     <value>
                       <struct>
                         <member>
                           <name>code</name><value><int>some int</int></value>
                         </member>
                         <member>
                           <name>message</name><value>some message string</value>
                         </member>
             </..close all elements>
        """
        node_param = self.find_node('param', xml_str=xml_str)
        node_param_value = self.find_node('value', parent=node_param)
        node_array = self.find_node('array', parent=node_param_value)
        # not an exception
        if node_array is None:
            return
        node_data = self.find_node('data', parent=node_array)
        node_data_value = self.find_node('value', parent=node_data)
        node_struct = self.find_node('struct', parent=node_data_value)
        node_struct_members = self.find_nodes('member', parent=node_struct)
        # check error found, not safe, silenced errors here
        if len(node_struct_members) != 2:
            return
        # 1º member
        node_value_one = self.find_node('value', parent=node_struct_members[0])
        node_value_type_one = self.find_node('int', parent=node_value_one)
        # 2º member
        node_value_second = self.find_node('value', parent=node_struct_members[1])
        node_value_type_second = self.find_node('string', parent=node_value_second)
        # build response error
        code = int(node_value_type_one.text)
        message = str(node_value_type_second.text)
        raise ResponseException(code, self.log, message=message)
