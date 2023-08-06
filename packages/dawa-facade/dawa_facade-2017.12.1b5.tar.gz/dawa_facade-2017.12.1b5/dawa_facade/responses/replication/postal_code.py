#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""postal_code.py
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Martin Storgaard Dieu <ms@intramanager.com>, november 2017
"""
import datetime

from dawa_facade.responses import BaseResponse, parse_datetime


class PostalCodeData(BaseResponse):
    """

    """

    def __init__(self, **kwargs) -> None:
        kwargs['postal_code'] = kwargs['nr']
        kwargs['name'] = kwargs['navn']
        kwargs['is_organisational'] = kwargs['stormodtager']
        del kwargs['nr']
        del kwargs['navn']
        del kwargs['stormodtager']
        super().__init__(**kwargs)

    @property
    def postal_code(self) -> str:
        """Unique identification of the postal code. Postal codes are defined by Post Danmark.

        :return: A four digit postal code, e.g. "2400" for "København NV” (nr)
        """
        return super().get('postal_code')

    @property
    def name(self) -> str:
        """The name attached to the postal code. This is typically the name of the city or neighbourhood.

        :return: A 20 character name, e.g. "København NV” (navn)
        """
        return super().get('name')

    @property
    def is_organisational(self) -> bool:
        """If the postal code is a special type attached to an organization.

        :return: True if the postal code is attached to an organisation, False otherwise
        """
        return super().get('is_organisational')


class PostalCodeEvent(BaseResponse):
    """A sequence number

    A unique sequence number for an event in DAWA

    """
    def __init__(self, **kwargs) -> None:
        kwargs['sequence_number'] = int(kwargs['sekvensnummer'])
        kwargs['timestamp'] = parse_datetime(kwargs['tidspunkt'])
        kwargs['operation'] = kwargs['operation'].lower()
        kwargs['data'] = PostalCodeData(**kwargs['data'])
        del kwargs['sekvensnummer']
        del kwargs['tidspunkt']
        super().__init__(**kwargs)

    @property
    def sequence_number(self) -> int:
        """The sequence number for the event

        :return: The sequence number (sekvensnummer)
        """
        return super().get('sequence_number')

    @property
    def timestamp(self) -> datetime.datetime:
        """The timestamp for the event

        :return: The timestamp (tidspunkt)
        """
        return super().get('timestamp')

    @property
    def operation(self) -> str:
        """The type of event: insert, update, delete

        :return: The type of the event (operation)
        """
        return super().get('operation')

    @property
    def data(self) -> PostalCodeData:
        """The data

        :return: The data (data)
        """
        return super().get('data')
