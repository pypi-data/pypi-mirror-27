#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""street.py
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Martin Storgaard Dieu <ms@intramanager.com>, november 2017
"""
import datetime

from dawa_facade.responses import BaseResponse, parse_datetime


class StreetData(BaseResponse):
    """

    """

    def __init__(self, **kwargs) -> None:
        kwargs['code'] = kwargs['kode']
        kwargs['municipality_code'] = kwargs['kommunekode']
        # Optional arguments
        kwargs['name'] = kwargs.get('navn', None)
        kwargs['addressing'] = kwargs.get('adresseringsnavn', None)

        del kwargs['kode']
        del kwargs['kommunekode']
        kwargs.pop('navn', None)
        kwargs.pop('adresseringsnavn', None)

        # The following fields are deprecated and are no longer updated
        kwargs.pop('oprettet', None)
        kwargs.pop('ændret', None)
        super().__init__(**kwargs)

    @property
    def code(self) -> str:
        """Identification of a street.

        It is unique within the municipality. It is represented by four digits.

        Example: "0004" is "Abel Cathrines Gade" in the municipality of Compenhagen.

        :return: The identification code of the street (kode)
        """
        return super().get('code')

    @property
    def municipality_code(self) -> str:
        """The municipality code.

        It is represented by four digits.

        :return: The municipality code (kommunekode)
        """
        return super().get('municipality_code')

    @property
    def name(self) -> str:
        """The name of the street.

        The name established and registered by the municipality. Represented with up to 40 characters, e.g.
        ”Hvidkildevej”

        :return: The name of the street (navn)
        """
        return super().get('name')

    @property
    def addressing(self) -> str:
        """A shorthand for the street name.

        Can be used for addressing on labels, window envelopes etc. Represented with at most 20 characters.

        :return: The addressing (adresseringsnavn)
        """
        return super().get('addressing')


class StreetEvent(BaseResponse):
    """A sequence number

    A unique sequence number for an event in DAWA

    """
    def __init__(self, **kwargs) -> None:
        kwargs['sequence_number'] = int(kwargs['sekvensnummer'])
        kwargs['timestamp'] = parse_datetime(kwargs['tidspunkt'])
        kwargs['data'] = StreetData(**kwargs['data'])
        kwargs['operation'] = kwargs['operation'].lower()
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
    def data(self) -> StreetData:
        """The data

        :return: The data (data)
        """
        return super().get('data')
