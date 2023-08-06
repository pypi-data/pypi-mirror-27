#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_streets.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import datetime
import unittest
from dawa_facade import DawaFacade
import requests_mock
import os.path
import os
from dawa_facade.responses.replication.street import StreetEvent, StreetData


class StreetTestCase(unittest.TestCase):
    """
    :type facade: DawaFacade
    """
    facade = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Check if we are testing online or offline (default)
        if 'TEST_ONLINE' not in os.environ:
            # We are testing OFFLINE. Get the absolute path to ./streets_10500_11500.json.gz
            mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'streets_10500_11500.json.gz')
            # Prepare the adapter to mock the requests
            adapter = requests_mock.Adapter()

            # Set the endpoint to be a captured response from the real api
            with open(mock_file, 'rb') as fp:
                adapter.register_uri(
                    method='GET',
                    url='mock://dawa.aws.dk/replikering/vejstykker/haendelser',
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

    def test_get_streets(self):
        """Test streets from 10500 to 11500 (9 events)
        """
        generator = self.facade.replication.get_streets(from_sequence_number=10500, to_sequence_number=11500)

        # Store each postal code
        streets = []
        for street in generator:
            # Check that marshall is working
            self.assertIsInstance(street, StreetEvent)
            # Store it to compare if we got what we expected
            streets.append(street)
        # Compare if we got what we expected
        self.assertListEqual(EXPECTED_STREETS_10500_11500, streets)
        # Test that accessing the properties works
        street = streets[0]  # type: StreetEvent
        expected_street = EXPECTED_STREETS_10500_11500[0]
        self.assertEqual(street.operation, expected_street['operation'])
        self.assertEqual(street.timestamp, expected_street['timestamp'])
        self.assertEqual(street.sequence_number, expected_street['sequence_number'])
        self.assertEqual(street.data.addressing, expected_street['data']['addressing'])
        self.assertEqual(street.data.municipality_code, expected_street['data']['municipality_code'])
        self.assertEqual(street.data.name, expected_street['data']['name'])
        self.assertEqual(street.data.code, expected_street['data']['code'])

    @unittest.skipIf('TEST_ONLINE' not in os.environ, "Add TEST_ONLINE to environment, e.g. export TEST_ONLINE=")
    def test_get_all_changes(self):
        """Test all events that has ever happened
        """
        # When calling with no parameters, we get all events that has ever happened
        generator = self.facade.replication.get_streets()

        last = next(generator)
        self.assertIsInstance(last, StreetEvent)
        for street in generator:
            # Check that the sequence numbers are ascending
            self.assertGreater(street.sequence_number, last.sequence_number)
            # Check that marshall is working
            self.assertIsInstance(street, StreetEvent)
            self.assertIsInstance(street.timestamp, datetime.datetime)
            self.assertIsInstance(street.sequence_number, int)
            self.assertIsInstance(street.data, StreetData)
            self.assertIsInstance(street.data.municipality_code, str)
            self.assertIsInstance(street.data.code, str)

            # Check that the street data satisfies the specification
            self.assertTrue(len(street.data.code) == 4, street.data.code)
            self.assertTrue(len(street.data.municipality_code) == 4, street.data.municipality_code)

            if street.data.name is not None:
                self.assertIsInstance(street.data.name, str)
                self.assertTrue(len(street.data.name) <= 40, street.data.name)
            if street.data.addressing is not None:
                self.assertTrue(len(street.data.addressing) <= 20, street.data.addressing)
                self.assertIsInstance(street.data.addressing, str)


EXPECTED_STREETS_10500_11500 = [

    {'data': {
        'code': '9902',
        'municipality_code': '0766',
        'name': 'Udrejst Nordisk Land',
        'addressing': 'Udrejst Nordisk Land'
    },
        'operation': 'update',
        'timestamp': datetime.datetime(2014, 8, 21, 20, 15, 34, 112000),
        'sequence_number': 10543
    },
    {'data': {
        'code': '2228',
        'municipality_code': '0751',
        'name': 'Frederiks Plads',
        'addressing': 'Frederiks Plads'
    },
        'operation': 'insert',
        'timestamp': datetime.datetime(2014, 8, 21, 20, 15, 34, 112000),
        'sequence_number': 10544
    },
    {'data': {
        'code': '2187',
        'municipality_code': '0791',
        'name': 'Hf. Fjeren',
        'addressing': 'Hf. Fjeren'
    },
        'operation': 'insert',
        'timestamp': datetime.datetime(2014, 8, 21, 20, 15, 34, 112000),
        'sequence_number': 10545
    },
    {'data': {
        'code': '2327',
        'municipality_code': '0810',
        'name': 'Risagerlundvej',
        'addressing': 'Risagerlundvej'
    },
        'operation': 'insert',
        'timestamp': datetime.datetime(2014, 8, 21, 20, 15, 34, 112000),
        'sequence_number': 10546
    },
    {'data': {
        'code': '2922',
        'municipality_code': '0540',
        'name': 'Mølleager',
        'addressing': 'Mølleager'
    },
        'operation': 'insert',
        'timestamp': datetime.datetime(2014, 8, 22, 20, 15, 31, 808000),
        'sequence_number': 11205
    },
    {'data': {
        'code': '2566',
        'municipality_code': '0376',
        'name': 'Digeparken',
        'addressing': 'Digeparken'
    },
        'operation': 'insert',
        'timestamp': datetime.datetime(2014, 8, 23, 20, 15, 41, 857000),
        'sequence_number': 11398
    },
    {'data': {
        'code': '6378',
        'municipality_code': '0101',
        'name': 'Sigynsgade',
        'addressing': 'Sigynsgade'
    },
        'operation': 'update',
        'timestamp': datetime.datetime(2014, 8, 26, 20, 15, 48, 203000),
        'sequence_number': 11415
    },
    {'data': {
        'code': '2113',
        'municipality_code': '0316',
        'name': 'Vipperød Byvej',
        'addressing': 'Vipperød Byvej'
    },
        'operation': 'insert',
        'timestamp': datetime.datetime(2014, 8, 26, 20, 15, 48, 203000),
        'sequence_number': 11416
    },
    {'data': {
        'code': '0643',
        'municipality_code': '0230',
        'name': 'Thalbitzersvej',
        'addressing': 'Thalbitzersvej'
    },
        'operation': 'delete',
        'timestamp': datetime.datetime(2014, 8, 26, 20, 15, 48, 203000),
        'sequence_number': 11417
    }
]
