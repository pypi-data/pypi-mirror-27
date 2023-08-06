#!/usr/bin/env python

import random,urlparse,cgi,logging,hmac,hashlib,base64
log = logging.getLogger(__name__)
try:
    import Cookie
except ImportError:
    from http import cookies as Cookie
try:
    import cPickle as pickle
except ImportError:
    import pickle
class WSGIMiddleware(object):
    """WSGI middleware application.

    :param client: oauth2 client
    :type client: :class:`Client`
    :param application: wsgi application
    :type application: callable object
    :param secret: secret key for generating HMAC signature
    :type secret: :class:`bytes`
    :param path: path prefix used for callback. by default, a randomly
                 generated complex path is used
    :type path: :class:`basestring`
    :param cookie: cookie name to be used for maintaining the user session.
                   default is :const:`DEFAULT_COOKIE`
    :type cookie: :class:`basestring`
    :param set_remote_user: Set to True to set the REMOTE_USER environment
                            variable to the authenticated username (if supported
                            by the :class:`Service`)
    :type set_remote_user: :class:`bool`
    :param forbidden_path: What path should be used to display the 403 Forbidden
                           page.  Any forbidden user will be redirected to this
                           path and a default 403 Forbidden page will be shown.
                           To override the default Forbidden page see the
                           ``forbidden_passthrough`` option.
    :type forbidden_path: :class:`basestring`
    :param forbidden_passthrough: Should the forbidden page be passed-through to
                                  the protected application. By default, a
                                  generic Forbidden page will be generated. Set
                                  this to :const:`True` to pass the request
                                  through to the protected application.
    :type forbidden_passthrough: :class:`bool`
    :param login_path:  The base path under which login will be required. Any
                        URL starting with this path will trigger the OAuth2
                        process.  The default is '/', meaning that the entire
                        application is protected.  To override the default
                        path see the :attr:`login_path` option.
    :type login_path: :class:`basestring`

    .. versionadded:: 0.1.4
       The ``login_path`` option.

    .. versionadded:: 0.1.3
       The ``forbidden_path`` and ``forbidden_passthrough`` options.

    .. versionadded:: 0.1.2
       The ``set_remote_user`` option.

    """

    #: (:class:`basestring`) The default name for :attr:`cookie`.
    DEFAULT_COOKIE = 'wsgioauth2sess'

    #: (:class:`Client`) The OAuth2 client.
    client = None

    #: (callable object) The wrapped WSGI application.
    application = None

    #: (:class:`bytes`) The secret key for generating HMAC signature.
    secret = None

    #: (:class:`basestring`) The path prefix for callback URL. It always
    #: starts and ends with ``'/'``.
    #path = "/"

    #: (:class:`basestring`) The path that is used to display the 403 Forbidden
    #: page.  Any forbidden user will be redirected to this path and a default
    #: 403 Forbidden page will be shown.  To override the default Forbidden
    #: page see the :attr:`forbidden_passthrough` option.
    forbidden_path = None

    #: (:class:`bool`) Whether the forbidden page should be passed-through
    #: to the protected application.   By default, a generic Forbidden page
    #: will be generated.  Set this to :const:`True` to pass the request
    #: through to the protected application.
    forbidden_passthrough = None

    #: (:class:`basestring`) The base path under which login will be required.
    #: Any URL starting with this path will trigger the OAuth2 process.  The
    #: default is '/', meaning that the entire application is protected.  To
    #: override the default path see the :attr:`login_path` option.
    #:
    #: .. versionadded:: 0.1.4
    login_path = None

    #: (:class:`basestring`) The cookie name to be used for maintaining
    #: the user session.
    cookie = None

    def __init__(self, client, application, secret,
                 path="/oauth2callback", cookie=DEFAULT_COOKIE, set_remote_user=True,
                 forbidden_path=None, forbidden_passthrough=False,
                 login_path='/session_login/'):
        #if not isinstance(client, Client):
        #    raise TypeError('client must be a wsgioauth2.Client instance, '
        #                    'not ' + repr(client))
        if not callable(application):
            raise TypeError('application must be an WSGI compliant callable, '
                            'not ' + repr(application))
        if not isinstance(secret, bytes):
            raise TypeError('secret must be bytes, not ' + repr(secret))
        if not (path is None or isinstance(path, basestring)):
            raise TypeError('path must be a string, not ' + repr(path))
        if not (forbidden_path is None or
                isinstance(forbidden_path, basestring)):
            raise TypeError('forbidden_path must be a string, not ' +
                            repr(path))
        if not (login_path is None or
                isinstance(login_path, basestring)):
            raise TypeError('login_path must be a string, not ' +
                            repr(path))
        if not isinstance(cookie, basestring):
            raise TypeError('cookie must be a string, not ' + repr(cookie))
        self.client = client
        #log.debug("client: %r"%self.client)
        self.application = application
        self.secret = secret
        if path is None:
            seq = ('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                   'abcdefghijklmnopqrstuvwxyz_-.')
            path = ''.join(random.choice(seq) for x in range(40))
            path = '__{0}__'.format(path)
        #self.path = '/{0}/'.format(path.strip('/'))
        self.path = path
        if forbidden_path is None:
            forbidden_path = "/forbidden"
        # forbidden_path must start with a / to avoid relative links
        if not forbidden_path.startswith('/'):
            forbidden_path = '/' + forbidden_path
        self.forbidden_path = forbidden_path
        self.forbidden_passthrough = forbidden_passthrough
        if login_path is None:
            login_path = '/'
        # login_path must start with a / to ensure proper matching
        if not login_path.startswith('/'):
            login_path = '/' + login_path
        self.login_path = login_path
        #log.debug("login path: %s"%self.login_path)
        self.cookie = cookie
        self.set_remote_user = set_remote_user

    def sign(self, value):
        """Generate signature of the given ``value``.

        .. versionadded:: 0.2.0

        """
        if not isinstance(value, bytes):
            raise TypeError('expected bytes, not ' + repr(value))
        return hmac.new(self.secret, value, hashlib.sha1).hexdigest()

    def redirect(self, url, start_response, headers={}):
        h = {'Content-Type': 'text/html; charset=utf-8', 'Location': url}
        h.update(headers)
        start_response('307 Temporary Redirect', list(h.items()))
        e_url = cgi.escape(url).encode('iso-8859-1')
        yield b'<!DOCTYPE html>'
        yield b'<html><head><meta charset="utf-8">'
        yield b'<meta http-equiv="refresh" content="0; url='
        yield e_url
        yield b'"><title>Redirect to '
        yield e_url
        yield b'</title></head><body><p>Redirect to <a href="'
        yield e_url
        yield b'">'
        yield e_url
        yield b'</a>&hellip;</p></body></html>'

    def forbidden(self, start_response):
        """Respond with an HTTP 403 Forbidden status."""
        h = [('Content-Type', 'text/html; charset=utf-8')]
        start_response('403 Forbidden', h)
        yield b'<!DOCTYPE html>'
        yield b'<html><head><meta charset="utf-8">'
        yield b'<title>Forbidden</title></head>'
        yield b'<body><p>403 Forbidden - '
        yield b'Your account does not have access to the requested resource.'
        yield b'<pre>'
        yield b'</pre>'
        yield b'</p></body></html>'

    def __call__(self, environ, start_response):
        url = '{0}://{1}{2}'.format(environ.get('wsgi.url_scheme', 'https'),
                                    environ.get('HTTP_HOST', ''),
                                    environ.get('PATH_INFO', '/'))
        
        #XXX use the proper redirect_uri 
        redirect_uri = urlparse.urljoin(url, self.path)
        forbidden_uri = urlparse.urljoin(url, self.forbidden_path)
        query_string = environ.get('QUERY_STRING', '')
        #log.debug("query string: %r" % query_string)
        if query_string:
            url += '?' + query_string
        cookie_dict = Cookie.SimpleCookie()
        cookie_dict.load(environ.get('HTTP_COOKIE', ''))
        query_dict = urlparse.parse_qs(query_string)
        path = environ['PATH_INFO']
        #log.debug("path=%r"%path)
        #log.debug("my path is %s" % self.path)
        if path.startswith(self.forbidden_path):
            if self.forbidden_passthrough:
                # Pass the forbidden request through to the app
                return self.application(environ, start_response)
            return self.forbidden(start_response)

        elif path.startswith(self.path):
            #log.debug("Path: %s"%self.path)
            code = query_dict.get('code')
            if not code:
                # No code in URL - forbidden
                return self.redirect(forbidden_uri, start_response)

            try:
                code = code[0]
                access_token = self.client.request_access_token(redirect_uri,
                                                                code)
            except TypeError:
                # No access token provided - forbidden
                return self.redirect(forbidden_uri, start_response)

            # Load the username now so it's in the session cookie
            log.debug(self.set_remote_user)
            if self.set_remote_user:
                log.debug("Setting remote user name now...")
                self.client.load_username(access_token)

            # Check if the authenticated user is allowed
            if not self.client.is_user_allowed(access_token):
                return self.redirect(forbidden_uri, start_response)

            session = pickle.dumps(access_token)
            
            sig = self.sign(session)
            signed_session = sig.encode('ascii') + b',' + session
            signed_session = base64.urlsafe_b64encode(signed_session)
            set_cookie = Cookie.SimpleCookie()
            set_cookie[self.cookie] = signed_session.decode('ascii')
            set_cookie[self.cookie]['path'] = '/'
            if 'expires_in' in access_token:
                expires_in = int(access_token['expires_in'])
                set_cookie[self.cookie]['expires'] = expires_in
            set_cookie = set_cookie[self.cookie].OutputString()
            return self.redirect(query_dict.get('state', [''])[0],
                                 start_response,
                                 headers={'Set-Cookie': set_cookie})
        elif path.startswith(self.login_path):
            #log.debug('trying login path')
            if self.cookie in cookie_dict:
                session = cookie_dict[self.cookie].value
                try:
                    session = base64.urlsafe_b64decode(session)
                except binascii.Error:
                    session = b''
                if b',' in session:
                    sig, val = session.split(b',', 1)
                    if sig.decode('ascii') == self.sign(val):
                        try:
                            session = pickle.loads(val)
                        except (pickle.UnpicklingError, ValueError):
                            session = None
                    else:
                        session = None
                else:
                    session = None
            else:
                session = None

            if session is None:
                return self.redirect(
                    self.client.make_authorize_url(redirect_uri, state=url),
                    start_response
                )
            else:
                environ = dict(environ)
                environ['wsgioauth2.session'] = session
                if self.set_remote_user and 'name' in session:
                    #log.debug('are you happy now??')
                    environ['REMOTE_USER'] = session['name']
        return self.application(environ, start_response)

