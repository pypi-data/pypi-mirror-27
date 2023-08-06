#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dawa_session.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import requests
import dawa_facade.util.exceptions


class DawaSession(requests.Session):
    def __init__(self, base_url: str, timeout):
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout

    def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                json=None, **kwargs):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.

        If the URL starts with / then the url is prefixed by the base url.

        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, bytes, or file-like object to send
            in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
        if url.startswith('/'):
            url = self.base_url + url

        timeout = self.timeout
        if 'timeout' in kwargs:
            timeout = kwargs['timeout']
        return super().request(method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects,
                               proxies, hooks, stream, verify, cert, json)

    def get(self, url, **kwargs) -> requests.Response:
        """Sends a GET request. Returns :class:`requests.Response` object.

        :param url: URL for the new :class:`requests.Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        """
        if 'stream' not in kwargs:
            kwargs['stream'] = True
        response = super().get(url, **kwargs)
        # Check that the content type is as expected
        content_type = response.headers.get('Content-Type', '** NOT IN RESPONSE HEADERS **')  # type: str
        if not content_type.startswith('application/json'):
            raise dawa_facade.util.exceptions.UnknownContentType(
                status_code=response.status_code,
                details={'expected': 'application/json', 'got': content_type}
            )
        # Check if we got an exception
        if response.status_code != 200:
            data = response.json()
            if response.status_code == 404 and isinstance(data, list) and len(data) == 0:
                # Not found but no error code
                return response

            if 'type' in data:
                # The type of the exception was provided by DAWA, check if we have implemented it
                exception_class = getattr(
                    o=dawa_facade.util.exceptions,
                    name=data['type'],
                    default=dawa_facade.util.exceptions.UnknownException
                )
                # No matter what, it is for sure a subclass of DawaException we have now
                assert issubclass(exception_class, dawa_facade.util.exceptions.DawaException)

                if 'details' in data:
                    # DAWA also provided details about the exception, include these
                    raise exception_class(status_code=response.status_code, details=data['details'])
                # No details
                raise exception_class(status_code=response.status_code)

            # Unknown type of exception
            raise dawa_facade.util.exceptions.UnknownException(status_code=response.status_code, details=data)

        # Yay, we got status code 200, everything must be fine
        return response
