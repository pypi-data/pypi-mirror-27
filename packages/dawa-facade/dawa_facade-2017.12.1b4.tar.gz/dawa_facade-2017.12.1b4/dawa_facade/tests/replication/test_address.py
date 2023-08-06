#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_addresss.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import datetime
import unittest
from dawa_facade import DawaFacade
import requests_mock
import os.path
import os
from dawa_facade.responses.replication.address import AddressEvent, AddressData


class AddressTestCase(unittest.TestCase):
    """
    :type facade: DawaFacade
    """
    facade = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Check if we are testing online or offline (default)
        if 'TEST_ONLINE' not in os.environ:
            # We are testing OFFLINE. Get the absolute path to ./addresss_10335_10340.json.gz
            mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'addresses_10335_10340.json.gz')
            # Prepare the adapter to mock the requests
            adapter = requests_mock.Adapter()

            # Set the endpoint to be a captured response from the real api
            with open(mock_file, 'rb') as fp:
                adapter.register_uri(
                    method='GET',
                    url='mock://dawa.aws.dk/replikering/adresser/haendelser',
                    headers={
                        'Access-Control-Allow-Origin': '*',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Encoding': 'gzip',
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Date': 'Fri, 01 Dec 2017 20:12:25 GMT',
                        # 'Transfer-Encoding': 'chunked',
                        'Vary': 'Accept-Encoding',
                        'Via': '1.1 d22f1ddd950fbdfcea783ac76322f641.cloudfront.net (CloudFront)',
                        'X-Amz-Cf-Id': 'CkOkWpRb0N9rBKvLO1H5VqJcQ5bN_RbLK6Bc1Qo_GaBpKa2BZI7Ccw==',
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

    def test_get_addresss(self):
        """Test addresss from 10335 to 10340 (5 events)
        """
        generator = self.facade.replication.get_addresses(from_sequence_number=10335, to_sequence_number=10340)

        # Store each postal code
        addresses = []
        for address in generator:
            # Check that marshall is working
            self.assertIsInstance(address, AddressEvent)
            # Store it to compare if we got what we expected
            addresses.append(address)

    @unittest.skipIf('TEST_ONLINE' not in os.environ, "Add TEST_ONLINE to environment, e.g. export TEST_ONLINE=")
    def test_get_all_changes(self):
        """Test all events that has ever happened
        """
        # When calling with no parameters, we get all events that has ever happened
        generator = self.facade.replication.get_addresses()

        last = next(generator)
        self.assertIsInstance(last, AddressEvent)
        for address in generator:
            # Check that the sequence numbers are ascending
            self.assertGreater(address.sequence_number, last.sequence_number)
            # Check that marshall is working
            self.assertIsInstance(address, AddressEvent)
            self.assertIsInstance(address.timestamp, datetime.datetime)
            self.assertIsInstance(address.sequence_number, int)
            self.assertIsInstance(address.data, AddressData)
