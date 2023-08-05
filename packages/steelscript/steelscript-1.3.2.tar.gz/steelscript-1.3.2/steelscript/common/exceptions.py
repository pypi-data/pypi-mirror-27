# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


import json
import xml.etree.ElementTree as ElementTree

__all__ = ['RvbdException', 'RvbdHTTPException']


class RvbdException(Exception):
    pass


class RvbdConnectException(RvbdException):
    def __init__(self, message, **kwargs):
        super(RvbdConnectException, self).__init__(message)
        self.errno = kwargs.get('errno', None)
        self.errname = kwargs.get('errname', None)


class RvbdHTTPException(RvbdException):
    def __init__(self, result, data, method, urlpath):
        RvbdException.__init__(
            self, ('HTTP %s on %s returned status %s (%s)' %
                   (method, urlpath, result.status_code, result.reason))
        )

        self.status = result.status_code
        self.reason = result.reason
        self.xresult = result
        self.xdata = data
        # Try to parse the error structure (either XML or JSON)
        try:
            t = result.headers.get('Content-type', None)
            if t == 'text/xml':
                e = ElementTree.fromstring(data)
                if e.tag != 'error':
                    if e.tag == 'TraceStats':
                        self.error_id = None
                        self.error_text = e.get('Cause')
                    else:
                        msg = 'Unable to parse error message from server'
                        raise ValueError(msg)
                else:
                    self.error_id = e.get('error_id')
                    self.error_text = e.get('error_text')

            elif t is not None and 'application/json' in t:
                d = json.loads(data)
                # for NetShark
                try:
                    self.error_text = d['error_text']
                    self.error_id = d['error_id']
                except KeyError:
                    # for NetProfiler
                    self.error_id = None
                    self.error_text = d['status_text']
            elif self.reason == 'Unauthorized':
                self.error_id = 'AUTH_REQUIRED'
                self.error_text = "Not authorized"
            else:
                self.error_id = None
                self.error_text = self.reason

            if self.error_text == "Not authorized":
                self.error_text += (
                    " You are not logged in. "
                    "Use the auth parameter to enter valid credentials or "
                    "authenticate using the .authenticate(auth) method."
                )

        except Exception, e:
            self.error_id = 'INVALID_ERROR_IDENTIFIER'
            self.error_text = e.message

    def __str__(self):
        return "%s %s" % (self.status, self.error_text)
