# Copyright (C) 2011-2014 by Hong Minhee <http://hongminhee.org/>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
""":mod:`wsgioauth2` --- Simple WSGI middleware for OAuth 2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a simple WSGI middleware that requires the user to
authenticate via the specific `OAuth 2.0`_ service e.g. Facebook_, Google_.

.. _OAuth 2.0: http://oauth.net/2/
.. _Facebook: http://www.facebook.com/
.. _Google: http://www.google.com/

"""
import base64
import binascii
import cgi
try:
    import Cookie
except ImportError:
    from http import cookies as Cookie
import hashlib
import hmac
try:
    import simplejson as json
except ImportError:
    import json
import numbers
try:
    import cPickle as pickle
except ImportError:
    import pickle
import random
try:
    import urllib2
except ImportError:
    from urllib import request as urllib2
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse
    urlencode = urlparse.urlencode
else:
    from urllib import urlencode

__author__ = 'Etienne Robillard'
__email__ = 'tkadm30' "@" 'yandex.ru'
__license__ = 'Apache'
__version__ = '0.2'
__copyright__ = '2016, Etienne Robillard'
__homepage__ = 'https://www.isotopesoftware.ca/software/django-hotsauce-oauthclient/'

__all__ = ('AccessToken', 'GitHubService', 'GithubService',
           'Service', 'WSGIMiddleware', 'github', 'google', 'facebook')


# Python 3 compatibility
try:
    basestring
except NameError:
    basestring = str



