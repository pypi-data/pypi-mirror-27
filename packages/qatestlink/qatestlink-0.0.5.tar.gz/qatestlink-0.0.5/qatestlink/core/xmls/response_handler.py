# -*- coding: utf-8 -*-
"""TODO: doc module"""


from xml.etree.ElementTree import tostring as xml_to_str
from qatestlink.core.xmls.base_handler import BaseHandler


class ResponseHandler(BaseHandler):
    """TODO: doc class"""

    def __init__(self, log):
        """Instance handler"""
        super(ResponseHandler, self).__init__(log)

    def create(self, route_type, xml_str):
        """Create response by router_type"""
        super(ResponseHandler, self).is_route_type(route_type)
        root = self.xml_parse(xml_str)
        return xml_to_str(root)

    def get_response_members(self, xml_str):
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
             </..close all elements>
        """
        node_param = self.find_node('param', xml_str=xml_str)
        node_param_value = self.find_node('array', parent=node_param)
        node_array = self.find_node('array', parent=node_param_value)
        node_data = self.find_node('data', parent=node_array)
        nodes_value = self.find_nodes('value', parent=node_data)
        res_members_list = list()
        for node_value in nodes_value:
            node_struct = self.find_node('struct', parent=node_value) # all okey
            # import pdb; pdb.set_trace()
            if node_struct is None:
                self.log.error("node_struct haven't <member> child tag")
            else:
                nodes_member = self.find_nodes('member', parent=node_struct)
                res_members = list()
                for node_member in nodes_member:
                    res_member = ResponseMember(self.log, node_member)
                    res_members.append(res_member)
                res_members_list.append(res_members)
        return res_members_list

    def get_response_struct_members(self, xml_str):
        """
        Allow to parse string XML object list response to
         ResponseMember object list
        :Args:
            xml_str: must be XML format string
             <param>
               <struct>
                 <member>
             </..close all elements>
        """
        node_param = self.find_node('param', xml_str=xml_str)
        node_struct = self.find_node('struct', parent=node_param)
        nodes_member = self.find_nodes('member', parent=node_struct)
        res_members = list()
        for node_member in nodes_member:
            res_member = ResponseMember(self.log, node_member)
            res_members.append(res_member)
        return res_members
        


class ResponseMember(BaseHandler):
    """
    Class to parse member XML node

    :usage:
        <member>
            <name>property_name</name>
            <value>
                <string>property_value</string>
            </value>
        </member>
    """

    _log = None
    _node_member = None

    name = None
    value = None

    def __init__(self, log, node_member, is_load=True):
        """TODO: doc method"""
        super(ResponseMember, self).__init__(log)
        if log is None:
            raise Exception('log param can\'t be None')
        self._log = log
        if node_member is None:
            raise Exception('node_member param can\'t be None')
        self._node_member = node_member
        if is_load:
            self._load()

    def _load(self):
        node_name = self.find_node(
            'name', parent=self._node_member)
        node_value = self.find_node(
            'value', parent=self._node_member)
        self.name = node_name.text
        self.value = self.parse_node_value(node_value)
        self.log.debug(
            'ResponseMember instance: name={}, value={}'.format(
                self.name, self.value))
