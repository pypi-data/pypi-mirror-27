#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""houseowners_association.py
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Martin Storgaard Dieu <ms@intramanager.com>, november 2017
"""
import datetime

from dawa_facade.responses import BaseResponse, parse_datetime


class HouseownersAssociationData(BaseResponse):
    """

    """

    def __init__(self, **kwargs) -> None:
        kwargs['code'] = int(kwargs.pop('kode'))
        kwargs['name'] = kwargs.pop('navn', None)
        super().__init__(**kwargs)

    @property
    def code(self) -> int:
        return super().get('code')

    @property
    def name(self) -> str:
        return super().get('name')


class HouseownersAssociationEvent(BaseResponse):
    """A sequence number

    A unique sequence number for an event in DAWA

    """
    def __init__(self, **kwargs) -> None:
        kwargs['sequence_number'] = int(kwargs['sekvensnummer'])
        kwargs['timestamp'] = parse_datetime(kwargs['tidspunkt'])
        kwargs['operation'] = kwargs['operation'].lower()
        kwargs['data'] = HouseownersAssociationData(**kwargs['data'])
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
    def data(self) -> HouseownersAssociationData:
        """The data

        :return: The data (data)
        """
        return super().get('data')
