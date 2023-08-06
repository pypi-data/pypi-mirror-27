#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_postal_codes.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import datetime
import unittest
from dawa_facade import DawaFacade
import requests_mock
import os.path
import os
from dawa_facade.responses.replication.postal_code import PostalCodeEvent, PostalCodeData


class PostalCodeTestCase(unittest.TestCase):
    """
    :type facade: DawaFacade
    """
    facade = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Check if we are testing online or offline (default)
        if 'TEST_ONLINE' not in os.environ:
            # We are testing OFFLINE. Get the absolute path to ./postal_codes_990_1000.json.gz
            mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postal_codes_990_1000.json.gz')
            # Prepare the adapter to mock the requests
            adapter = requests_mock.Adapter()

            # Set the endpoint to be a captured response from the real api
            with open(mock_file, 'rb') as fp:
                adapter.register_uri(
                    method='GET',
                    url='mock://dawa.aws.dk/replikering/postnumre/haendelser',
                    headers={
                        'Access-Control-Allow-Origin': '*',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Encoding': 'gzip',
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Date': 'Fri, 10 Nov 2017 21:14:38 GMT',
                        # TODO: Get the transfer encoding header to work correctly
                        # 'Transfer-Encoding': 'chunked',
                        'Vary': 'Accept-Encoding',
                        'Via': '1.1 11a727876922c83c000e3ada668fa181.cloudfront.net (CloudFront)',
                        'X-Amz-Cf-Id': 'a9o_RA7jz9_zK9Zq3HeVeb47JNg0VVzbFJsBh6q6bGQZhbZ5_J5hNA==',
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

    def test_get_postal_codes(self):
        """Test postal codes from 990 to 1000
        """
        generator = self.facade.replication.get_postal_codes(from_sequence_number=990, to_sequence_number=1000)

        # Store each postal code
        postal_codes = []
        for postal_code in generator:
            # Check that marshall is working
            self.assertIsInstance(postal_code, PostalCodeEvent)
            # Store it to compare if we got what we expected
            postal_codes.append(postal_code)
        # Compare if we got what we expected
        self.assertListEqual(EXPECTED_POSTAL_CODES_990_1000, postal_codes)

    @unittest.skipIf('TEST_ONLINE' not in os.environ, "Add TEST_ONLINE to environment, e.g. export TEST_ONLINE=")
    def test_get_all_changes(self):
        # When calling with no parameters, we get all events that has ever happened
        generator = self.facade.replication.get_postal_codes()

        last = next(generator)
        self.assertIsInstance(last, PostalCodeEvent)
        for postal_code in generator:
            # Check that the sequence numbers are ascending
            self.assertGreater(postal_code.sequence_number, last.sequence_number)
            # Check that marshall is working
            self.assertIsInstance(postal_code, PostalCodeEvent)
            self.assertIsInstance(postal_code.timestamp, datetime.datetime)
            self.assertIsInstance(postal_code.sequence_number, int)
            self.assertIsInstance(postal_code.data, PostalCodeData)
            self.assertIsInstance(postal_code.data.postal_code, str)
            self.assertIsInstance(postal_code.data.name, str)
            self.assertIsInstance(postal_code.data.is_organisational, bool)

            # Check that the postal code satisfies the specification
            self.assertTrue(len(postal_code.data.postal_code) == 4, postal_code.data.postal_code)
            # Check that the name satisfies the specification
            self.assertTrue(len(postal_code.data.name) <= 20, postal_code.data.name)


EXPECTED_POSTAL_CODES_990_1000 = [

    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Sorring',
            'postal_code': '8641',
            'is_organisational': False
        },
        'sequence_number': 990
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Ans By',
            'postal_code': '8643',
            'is_organisational': False
         },
        'sequence_number': 991
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Them',
            'postal_code': '8653',
            'is_organisational': False
        },
        'sequence_number': 992
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Bryrup',
            'postal_code': '8654',
            'is_organisational': False
        },
        'sequence_number': 993
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Skanderborg',
            'postal_code': '8660',
            'is_organisational': False
        },
        'sequence_number': 994
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Låsby',
            'postal_code': '8670',
            'is_organisational': False
        },
        'sequence_number': 995
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Ry',
            'postal_code': '8680',
            'is_organisational': False
        },
        'sequence_number': 996
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Horsens',
            'postal_code': '8700',
            'is_organisational': False
        },
        'sequence_number': 997
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Daugård',
            'postal_code': '8721',
            'is_organisational': False
        },
        'sequence_number': 998
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Hedensted',
            'postal_code': '8722',
            'is_organisational': False
        },
        'sequence_number': 999
    },
    {
        'timestamp': datetime.datetime(2014, 8, 20, 11, 17, 50, 644000),
        'operation': 'insert',
        'data': {
            'name': 'Løsning',
            'postal_code': '8723',
            'is_organisational': False
        },
        'sequence_number': 1000
    }
]
