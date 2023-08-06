# -*- coding: utf-8 -*-
"""TODO: doc module"""


from qatestlink.core.xmls.base_handler import BaseHandler
from xml.etree.ElementTree import tostring as xml_to_str


MSG_CREATED_XMLREQUEST = "Created XML request: \n {}"
MSG_CREATED_XMLPARAM = "Created XML param: \n {}"


class RequestHandler(BaseHandler):
    """TODO: doc class"""

    def __init__(self, log):
        """Instance handler"""
        super(RequestHandler, self).__init__(log)

    def create(self, route_type):
        """
        Create XML string ready to use
         on requests
        """
        super(RequestHandler, self).is_route_type(route_type)
        root = self.create_node('methodCall')
        self.create_node(
            'methodName', parent=root, text=route_type.value)
        self.create_node('params', parent=root)
        self.log.info(MSG_CREATED_XMLREQUEST.format(xml_to_str(root)))
        return xml_to_str(root)

    def create_param(self, req_str, param_type, param_name, param_value):
        """
        Add param to created xml request
         obtained as string
        """
        root = self.xml_parse(req_str)
        self.log.debug("Creating param:")
        self.log.debug("    type={}".format(param_type))
        self.log.debug("    name={}".format(param_name))
        self.log.debug("    value={}".format(param_value))
        n_params = self.find_node('params', parent=root)
        n_param = self.create_node('param', parent=n_params)
        n_value = self.create_node('value', parent=n_param)
        # TODO: type XML validation for params
        # just struct handleded
        if param_type == 'struct':
            n_struct = self.create_node('struct', parent=n_value)
            n_member = self.create_node('member', parent=n_struct)
            n_name = self.create_node(
                'name', parent=n_member, text=param_name)
            n_value = self.create_node('value', parent=n_member)
            n_value_string = self.create_node(
                'string', parent=n_value, text=param_value)
        else:
            raise Exception('param_type not supported, can\'t add_param')
        self.log.info(MSG_CREATED_XMLPARAM.format(xml_to_str(root)))
        return xml_to_str(root)

    def add_param(self, req_str, param_name, param_value):
        """
        Add param to created xml request
         obtained as string
        """
        """
        Add param to created xml request
         obtained as string
        """
        root = self.xml_parse(req_str)
        # need to parse ints to string 
        #  before to use on XMLs strings
        param_value = str(param_value) 
        self.log.debug("Adding param:")
        self.log.debug("    name={}".format(param_name))
        self.log.debug("    value={}".format(param_value))
        n_params = self.find_node('params', parent=root)
        n_param = self.find_node('param', parent=n_params)
        n_value = self.find_node('value', parent=n_param)
        # type XML validation for params
        #  just struct handled
        n_struct = self.find_node('struct', parent=n_value)
        n_member = self.create_node('member', parent=n_struct)
        self.create_node('name', parent=n_member, text=param_name)
        n_value = self.create_node('value', parent=n_member)
        self.create_node('string', parent=n_value, text=param_value)
        self.log.info(MSG_CREATED_XMLPARAM.format(xml_to_str(root)))
        return xml_to_str(root)