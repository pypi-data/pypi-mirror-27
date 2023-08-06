#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_access_addresss.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import datetime
import unittest
from dawa_facade import DawaFacade
import requests_mock
import os.path
import os
from dawa_facade.responses.replication.access_address import AccessAddressEvent, AccessAddressData


class AccessAddressTestCase(unittest.TestCase):
    """
    :type facade: DawaFacade
    """
    facade = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Check if we are testing online or offline (default)
        if 'TEST_ONLINE' not in os.environ:
            # We are testing OFFLINE. Get the absolute path to ./access_addresss_10500_11500.json.gz
            mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_addresses_10100_10140.json.gz')
            # Prepare the adapter to mock the requests
            adapter = requests_mock.Adapter()

            # Set the endpoint to be a captured response from the real api
            with open(mock_file, 'rb') as fp:
                adapter.register_uri(
                    method='GET',
                    url='mock://dawa.aws.dk/replikering/adgangsadresser/haendelser',
                    headers={
                        'Access-Control-Allow-Origin': '*',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Encoding': 'gzip',
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Date': 'Sat, 11 Nov 2017 20:16:22 GMT',
                        # 'Transfer-Encoding': 'chunked',
                        'Vary': 'Accept-Encoding',
                        'Via': '1.1 5cff1d1d173e3df63e9a43193891ff1b.cloudfront.net (CloudFront)',
                        'X-Amz-Cf-Id': 'XnYc_SZeah28KXLs1p96cNbAhAsMIIXhNl8vU4nRsR8vu6RC2eoenw==',
                        'X-Cache': 'Miss from cloudfront',
                        'X-Powered-By': 'Express'
                    },
                    status_code=200,
                    content=fp.read()
                )

            # Create the Facade using the mock address and mock adapter
            cls.facade = DawaFacade(base_url='mock://dawa.aws.dk')
            cls.facade.session.mount(prefix='mock://', adapter=adapter)
        else:
            # We are testing ONLINE, so just initialize the facade with default arguments
            cls.facade = DawaFacade()

    @classmethod
    def tearDownClass(cls):
        if isinstance(cls.facade, DawaFacade):
            # Clean up
            del cls.facade
        super().tearDownClass()

    def test_get_access_addresss(self):
        """Test access_addresss from 10100 to 10140 (9 events)
        """
        generator = self.facade.replication.get_access_addresses(from_sequence_number=10100, to_sequence_number=10140)

        # Store each postal code
        access_addresses = []
        for access_address in generator:
            # Check that marshall is working
            self.assertIsInstance(access_address, AccessAddressEvent)
            # Store it to compare if we got what we expected
            access_addresses.append(access_address)

    @unittest.skipIf('TEST_ONLINE' not in os.environ, "Add TEST_ONLINE to environment, e.g. export TEST_ONLINE=")
    def test_get_all_changes(self):
        """Test all events that has ever happened
        """
        # When calling with no parameters, we get all events that has ever happened
        generator = self.facade.replication.get_access_addresses()

        last = next(generator)
        self.assertIsInstance(last, AccessAddressEvent)
        for access_address in generator:
            # Check that the sequence numbers are ascending
            self.assertGreater(access_address.sequence_number, last.sequence_number)
            # Check that marshall is working
            self.assertIsInstance(access_address, AccessAddressEvent)
            self.assertIsInstance(access_address.timestamp, datetime.datetime)
            self.assertIsInstance(access_address.sequence_number, int)
            self.assertIsInstance(access_address.data, AccessAddressData)
