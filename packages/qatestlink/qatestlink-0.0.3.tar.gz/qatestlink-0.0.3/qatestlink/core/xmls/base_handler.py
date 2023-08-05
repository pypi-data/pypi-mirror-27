# -*- coding: utf-8 -*-
"""TODO: doc module"""


from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import fromstring as xml_from_str
from qatestlink.core.xmls.route_type import RouteType


MSG_CREATED_ELEMENT = "Created element named: '{}'"
MSG_CREATED_SUBELEMENT = "Created subelement named: parent='{}',  tag='{}'"
MSG_ADDED_TEXT = "Added text to element: tag='{}', text='{}'"
MSG_FOUND_NODE = "Found node: tag='{}', text='{}'"
MSG_ROUTE_TYPE_OK = "Valid route_type: '{}'"


class BaseHandler(object):
    """TODO: doc class"""
    log = None

    def __init__(self, log):
        """Instance handler"""
        self.log = log

    def is_route_type(self, route_type):
        """
        This method functionality must be
         complete at inherit classes
        """
        if not isinstance(route_type, RouteType):
            raise Exception('Bad RouteType : {}'.format(route_type))
        self.log.info(MSG_ROUTE_TYPE_OK.format(route_type))
        return True

    def create_node(self, tag, parent=None, text=None):
        """
        Create XML node element
         and subelement if parent is obtained
        """
        node = None
        if parent is None:
            node = Element(tag)
            self.log.debug(
                MSG_CREATED_ELEMENT.format(tag))
        else:
            node = SubElement(parent, tag)
            self.log.debug(
                MSG_CREATED_SUBELEMENT.format(parent.tag, tag))
        if text is not None:
            node.text = text
            self.log.debug(
                MSG_ADDED_TEXT.format(tag, text))
        return node

    def find_node(self, tag, xml_str=None, parent=None):
        """
        Returns firt node obtained iter
         by tag name on string 'request'
        """
        err_msg = 'Can\'t use this function like this, read documentation'
        if xml_str is None and parent is None:
            raise Exception(err_msg)
        if xml_str is not None and parent is not None:
            raise Exception(err_msg)
        if parent is not None:
            root = parent
        if xml_str is not None:
            root = self.xml_parse(xml_str)
        # Search element
        for node in ElementTree(element=root).iter(tag=tag):
            if node.tag == tag:
                self.log.debug(MSG_FOUND_NODE.format(node.tag, node.text))
                return node

    def find_nodes(self, tag, xml_str=None, parent=None):
        """
        Returns list of nodes obtained itering
         by tag name on string 'request'
        """
        err_msg = 'Can\'t use this function like this, read documentation'
        if xml_str is None and parent is None:
            raise Exception(err_msg)
        if xml_str is not None and parent is not None:
            raise Exception(err_msg)
        if parent is not None:
            root = parent
        if xml_str is not None:
            root = self.xml_parse(xml_str)
        # Search element
        nodes_found = list()
        for node in ElementTree(element=root).iter(tag=tag):
            if node.tag == tag:
                self.log.debug(MSG_FOUND_NODE.format(node.tag, node.text))
                nodes_found.append(node)
        return nodes_found

    def parse_node_value(self, node_value):
        """
        Parse and validate XML value member and return it
         parsed to each valid type
        """
        value_node_string = self.find_node(
            'string', parent=node_value)
        value_node_struct = self.find_node(
            'string', parent=node_value)
        if value_node_string is not None:
            return value_node_string.text
        if value_node_struct is not None:
            # TODO: i don't know how to do this yet
            raise NotImplementedError(
                'Response node_member struct not handled yet')


    def xml_parse(self, xml_str):
        """
        Parse request string and return it
        """
        self.log.debug("Parsing xml:")
        self.log.debug("    from={}".format(xml_str))
        root = ElementTree(xml_from_str(xml_str)).getroot()
        self.log.debug("    to={}".format(root))
        return root
