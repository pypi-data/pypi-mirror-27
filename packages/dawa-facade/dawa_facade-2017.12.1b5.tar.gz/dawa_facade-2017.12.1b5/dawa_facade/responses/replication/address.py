#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""address.py
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Martin Storgaard Dieu <ms@intramanager.com>, december 2017
"""
import datetime
import uuid

from dawa_facade.responses import BaseResponse, parse_datetime


class AddressData(BaseResponse):
    """

    """

    def __init__(self, **kwargs) -> None:
        kwargs['id'] = uuid.UUID(kwargs['id'])
        kwargs['status'] = int(kwargs['status'])
        kwargs['access_address_id'] = uuid.UUID(kwargs.pop('adgangsadresseid'))
        # Optionals
        kwargs['created_datetime'] = parse_datetime(kwargs.pop('oprettet', None))
        kwargs['updated_datetime'] = parse_datetime(kwargs.pop('ændret', None))
        kwargs['commencement_datetime'] = parse_datetime(kwargs.pop('ikrafttrædelsesdato', None))
        kwargs['floor'] = kwargs.pop('etage', None)
        kwargs['door'] = kwargs.pop('dør', None)
        kwargs['source'] = kwargs.pop('kilde', None)
        kwargs['esdh_reference'] = kwargs.pop('esdhreference', None)
        kwargs['journal_number'] = kwargs.pop('journalnummer', None)
        super().__init__(**kwargs)

    @property
    def id(self) -> uuid.UUID:
        return super().get('id')

    @property
    def status(self) -> int:
        return super().get('status')

    @property
    def access_address_id(self) -> uuid.UUID:
        return super().get('access_address_id')

    @property
    def created_datetime(self) -> datetime.datetime:
        return super().get('created_datetime')

    @property
    def updated_datetime(self) -> datetime.datetime:
        return super().get('updated_datetime')

    @property
    def commencement_datetime(self) -> datetime.datetime:
        return super().get('commencement_datetime')

    @property
    def floor(self) -> str:
        return super().get('floor')

    @property
    def door(self) -> str:
        return super().get('door')

    @property
    def source(self) -> str:
        return super().get('source')

    @property
    def esdh_reference(self) -> str:
        return super().get('esdh_reference')

    @property
    def journal_number(self) -> str:
        return super().get('journal_number')


class AddressEvent(BaseResponse):
    """A address event

    """
    def __init__(self, **kwargs) -> None:
        kwargs['sequence_number'] = int(kwargs['sekvensnummer'])
        kwargs['timestamp'] = parse_datetime(kwargs['tidspunkt'])
        kwargs['operation'] = kwargs['operation'].lower()
        kwargs['data'] = AddressData(**kwargs['data'])
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
    def data(self) -> AddressData:
        """The data

        :return: The data (data)
        """
        return super().get('data')
