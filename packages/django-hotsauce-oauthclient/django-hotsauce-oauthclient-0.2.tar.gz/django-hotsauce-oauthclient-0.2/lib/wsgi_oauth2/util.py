#!/usr/bin/env python

import urllib2


class AccessToken(dict):
    """Dictionary that contains access token. It always has ``'access_token'``
    key.

    """

    def __init__(self, *args, **kwargs):
        super(AccessToken, self).__init__(*args, **kwargs)
        if 'access_token' not in self:
            raise TypeError("'access_token' is required")

    @property
    def access_token(self):
        """(:class:`basestring`) Access token."""
        access_token = self['access_token']
        if isinstance(access_token, list):
            return access_token[0]
        return access_token

    def get(self, url, headers={}):
        """Requests ``url`` as ``GET``.

        :param headers: additional headers
        :type headers: :class:`collections.Mapping`

        """
        url += '&' if '?' in url else '?' + 'access_token=' + self.access_token
        request = urllib2.Request(url, headers=headers)
        return urllib2.urlopen(request)

    def post(self, url, form={}, headers={}):
        """Requests ``url`` as ``POST``.

        :param form: form data
        :type form: :class:`collections.Mapping`
        :param headers: additional headers
        :type headers: :class:`collections.Mapping`

        """
        form = dict(form)
        form['access_token'] = self.access_token
        request = urllib2.Request(url, data=form, headers=headers)
        return urllib2.urlopen(request)

    def __str__(self):
        return self.access_token

    def __repr__(self):
        cls = type(self)
        repr_ = dict.__repr__(self)
        return '{0}.{1}({2})'.format(cls.__module__, cls.__name__, repr_)

