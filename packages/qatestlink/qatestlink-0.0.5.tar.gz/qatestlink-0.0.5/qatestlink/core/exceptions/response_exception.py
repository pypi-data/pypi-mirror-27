# -*- coding: utf-8 -*-
"""TODO: doc module"""


class ResponseException(Exception):
    """Inherits exception, just for raises testlink XMLRPC errors"""

    def __init__(self, code, log,
                 message='Response Exception message not defined at raise',
                 err=None):
        """Raise an exception from any part of qacode package"""
        super(ResponseException, self).__init__(err, message)
        self._code = code
        self._message = message
        log.error(
            "Response exception detected: \n    code={}\n    message={}".format(
                self._code, self._message))
