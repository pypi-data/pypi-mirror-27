#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_street_postal_code_relations.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import datetime
import unittest
from dawa_facade import DawaFacade
import requests_mock
import os.path
import os
from dawa_facade.responses.replication.street_postal_code_relation import StreetPostalCodeRelationEvent, StreetPostalCodeRelationData


class StreetPostalCodeRelationTestCase(unittest.TestCase):
    """
    https://dawa.aws.dk/replikering/vejstykkepostnummerrelationer/haendelser?sekvensnummerfra=42670510&sekvensnummertil=42670514

    :type facade: DawaFacade
    """
    facade = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Check if we are testing online or offline (default)
        if 'TEST_ONLINE' not in os.environ:
            # We are testing OFFLINE. Get the absolute path to ./street_postal_code_relations_42670510_42670514.json.gz
            mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'street_postal_code_relations_42670510_42670514.json.gz')
            # Prepare the adapter to mock the requests
            adapter = requests_mock.Adapter()

            # Set the endpoint to be a captured response from the real api
            with open(mock_file, 'rb') as fp:
                adapter.register_uri(
                    method='GET',
                    url='mock://dawa.aws.dk/replikering/vejstykkepostnummerrelationer/haendelser',
                    headers={
                        'Access-Control-Allow-Origin': '*',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Encoding': 'gzip',
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Date': 'Fri, 08 Dec 2017 20:06:44 GMT',
                        # 'Transfer-Encoding': 'chunked',
                        'Vary': 'Accept-Encoding',
                        'Via': '1.1 051783ccfb83d3017740509521063835.cloudfront.net (CloudFront)',
                        'X-Amz-Cf-Id': '7MEQdiK-xYlBeQdAi5gMd8mSOXzCIZd5gG5lJnnv4Cy0WydWUo2wlg==',
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

    def test_get_street_postal_code_relations(self):
        """Test street_postal_code_relations from 42670510 to 42670514 (5 events)
        """
        generator = self.facade.replication.get_street_postal_code_relations(from_sequence_number=42670510, to_sequence_number=42670514)

        # Store each postal code
        street_postal_code_relations = []
        for street_postal_code_relation in generator:
            # Check that marshall is working
            self.assertIsInstance(street_postal_code_relation, StreetPostalCodeRelationEvent)
            # Store it to compare if we got what we expected
            street_postal_code_relations.append(street_postal_code_relation)
        # Compare if we got what we expected
        self.assertListEqual(EXPECTED_STREETS_42670510_42670514, street_postal_code_relations)
        # Test that accessing the properties works
        street_postal_code_relation = street_postal_code_relations[0]  # type: StreetPostalCodeRelationEvent
        expected_street_postal_code_relation = EXPECTED_STREETS_42670510_42670514[0]
        self.assertEqual(street_postal_code_relation.operation, expected_street_postal_code_relation['operation'])
        self.assertEqual(street_postal_code_relation.timestamp, expected_street_postal_code_relation['timestamp'])
        self.assertEqual(street_postal_code_relation.sequence_number, expected_street_postal_code_relation['sequence_number'])
        self.assertEqual(street_postal_code_relation.data.municipality_code, expected_street_postal_code_relation['data']['municipality_code'])
        self.assertEqual(street_postal_code_relation.data.street_code, expected_street_postal_code_relation['data']['street_code'])
        self.assertEqual(street_postal_code_relation.data.postal_code, expected_street_postal_code_relation['data']['postal_code'])

    @unittest.skipIf('TEST_ONLINE' not in os.environ, "Add TEST_ONLINE to environment, e.g. export TEST_ONLINE=")
    def test_get_all_changes(self):
        """Test all events that has ever happened
        """
        # When calling with no parameters, we get all events that has ever happened
        generator = self.facade.replication.get_street_postal_code_relations()

        last = next(generator)
        self.assertIsInstance(last, StreetPostalCodeRelationEvent)
        for street_postal_code_relation in generator:
            # Check that the sequence numbers are ascending
            self.assertGreater(street_postal_code_relation.sequence_number, last.sequence_number)
            # Check that marshall is working
            self.assertIsInstance(street_postal_code_relation, StreetPostalCodeRelationEvent)
            self.assertIsInstance(street_postal_code_relation.timestamp, datetime.datetime)
            self.assertIsInstance(street_postal_code_relation.sequence_number, int)
            self.assertIsInstance(street_postal_code_relation.data, StreetPostalCodeRelationData)
            self.assertIsInstance(street_postal_code_relation.data.municipality_code, str)
            self.assertIsInstance(street_postal_code_relation.data.street_code, str)
            self.assertIsInstance(street_postal_code_relation.data.postal_code, str)

            # Check that the street_postal_code_relation data satisfies the specification
            self.assertTrue(len(street_postal_code_relation.data.municipality_code) == 4, street_postal_code_relation.data.municipality_code)
            self.assertTrue(len(street_postal_code_relation.data.street_code) == 4, street_postal_code_relation.data.street_code)
            self.assertTrue(len(street_postal_code_relation.data.postal_code) == 4, street_postal_code_relation.data.postal_code)


EXPECTED_STREETS_42670510_42670514 = [
    {
        'operation': 'insert',
        'sequence_number': 42670510,
        'data': {
            'street_code': '1328',
            'municipality_code': '0710',
            'postal_code': '8370'
        },
        'timestamp': datetime.datetime(2017, 11, 30, 3, 4, 22, 248000)
    }, {
        'operation': 'insert',
        'sequence_number': 42670511,
        'data': {
            'street_code': '2897',
            'municipality_code': '0540',
            'postal_code': '6400'
        },
        'timestamp': datetime.datetime(2017, 11, 30, 3, 4, 22, 248000)
    }, {
        'operation': 'insert',
        'sequence_number': 42670512,
        'data': {
            'street_code': '3028',
            'municipality_code': '0370',
            'postal_code': '4700'
        },
        'timestamp': datetime.datetime(2017, 11, 30, 3, 4, 22, 248000)
    }, {
        'operation': 'insert',
        'sequence_number': 42670513,
        'data': {
            'street_code': '3024',
            'municipality_code': '0370',
            'postal_code': '4171'
        },
        'timestamp': datetime.datetime(2017, 11, 30, 3, 4, 22, 248000)
    }, {
        'operation': 'insert',
        'sequence_number': 42670514,
        'data': {
            'street_code': '1008',
            'municipality_code': '0210',
            'postal_code': '3480'
        },
        'timestamp': datetime.datetime(2017, 11, 30, 3, 4, 22, 248000)
    }
]
