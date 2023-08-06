#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_houseowners_association.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import datetime
import unittest
from dawa_facade import DawaFacade
import requests_mock
import os.path
import os
from dawa_facade.responses.replication.houseowners_association import HouseownersAssociationEvent, HouseownersAssociationData


class HouseownersAssociationTestCase(unittest.TestCase):
    """
    :type facade: DawaFacade
    """
    facade = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Check if we are testing online or offline (default)
        if 'TEST_ONLINE' not in os.environ:
            # We are testing OFFLINE. Get the absolute path to ./houseowners_association_1090_1100.json.gz
            mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'houseowners_association_1090_1100.json.gz')
            # Prepare the adapter to mock the requests
            adapter = requests_mock.Adapter()

            # Set the endpoint to be a captured response from the real api
            with open(mock_file, 'rb') as fp:
                adapter.register_uri(
                    method='GET',
                    url='mock://dawa.aws.dk/replikering/ejerlav/haendelser',
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

            # Create the Facade using the mock houseowners_association and mock adapter
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

    def test_get_houseowners_association(self):
        """Test houseowners_association from 1090 to 1100 (5 events)
        """
        generator = self.facade.replication.get_houseowners_association(from_sequence_number=1090, to_sequence_number=1100)

        # Store each postal code
        houseowners_associations = []
        for houseowners_association in generator:
            # Check that marshall is working
            self.assertIsInstance(houseowners_association, HouseownersAssociationEvent)
            # Store it to compare if we got what we expected
            houseowners_associations.append(houseowners_association)

    @unittest.skipIf('TEST_ONLINE' not in os.environ, "Add TEST_ONLINE to environment, e.g. export TEST_ONLINE=")
    def test_get_all_changes(self):
        """Test all events that has ever happened
        """
        # When calling with no parameters, we get all events that has ever happened
        generator = self.facade.replication.get_houseowners_association()

        last = next(generator)
        self.assertIsInstance(last, HouseownersAssociationEvent)
        for houseowners_association in generator:
            # Check that the sequence numbers are ascending
            self.assertGreater(houseowners_association.sequence_number, last.sequence_number)
            # Check that marshall is working
            self.assertIsInstance(houseowners_association, HouseownersAssociationEvent)
            self.assertIsInstance(houseowners_association.timestamp, datetime.datetime)
            self.assertIsInstance(houseowners_association.sequence_number, int)
            self.assertIsInstance(houseowners_association.data, HouseownersAssociationData)
