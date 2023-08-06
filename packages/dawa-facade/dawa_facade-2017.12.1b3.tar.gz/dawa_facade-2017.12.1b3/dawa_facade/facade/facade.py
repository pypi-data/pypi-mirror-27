#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""facade.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
from dawa_facade.facade.replication import Replication
from dawa_facade.util.dawa_session import DawaSession


class DawaFacade(object):
    def __init__(self, base_url: str=None, timeout=305):
        """Danmarks Adressers Web API (DAWA) provides data and functionality regarding the addresses, access addresses,
        street names and postal codes in Denmark. DAWA enables address functionality in it systems.

        This facade aims to keep everything simple and in english. This is a personal preference of the author, since
        this avoids strange things from happening with special characters etc. I also like to keep the code base in one
        language.

        :param base_url: The base url without trailing slash. Defaults to https://dawa.aws.dk
        :param float | (float, float) timeout: How long to wait for the server to send data before giving up, as a float, or a (connect timeout, read timeout) tuple
        """
        self.timeout = timeout

        if isinstance(base_url, str):
            self.base_url = base_url
        else:
            self.base_url = 'https://dawa.aws.dk'

        self.session = self._create_session()
        self.replication = Replication(self.session)

    def _create_session(self) -> DawaSession:
        """Creates a new session used for all subsequent calls

        :return: The new session
        """
        # Create the User-Agent so DAWA knows that we made the request
        from dawa_facade import __version__
        ua = 'Mozilla/5.0 (compatible; Dawa-Facade/{version:s}; +https://github.com/YnkDK/Dawa-Facade)'.format(
            version=__version__
        )

        # Create the session
        session = DawaSession(base_url=self.base_url, timeout=self.timeout)
        session.headers.update({
            'User-Agent': ua,
            'Accept': 'application/json'
        })
        return session

    def __del__(self):
        """Clean up after us

        Closes all adapters and such the session
        """
        if isinstance(self.session, DawaSession):
            self.session.close()
