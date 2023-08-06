#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""access_address.py
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Martin Storgaard Dieu <ms@intramanager.com>, november 2017
"""
import datetime
import uuid

from dawa_facade.responses import BaseResponse, parse_datetime


class AccessAddressData(BaseResponse):
    """

    """

    def __init__(self, **kwargs) -> None:
        kwargs['id'] = uuid.UUID(kwargs['id'])
        kwargs['status'] = int(kwargs['status'])
        kwargs['accuracy'] = kwargs.pop('nøjagtighed')

        # Optionals
        kwargs['created_datetime'] = parse_datetime(kwargs.pop('oprettet', None))
        kwargs['updated_datetime'] = parse_datetime(kwargs.pop('ændret', None))
        kwargs['commencement_datetime'] = parse_datetime(kwargs.pop('ikrafttrædelsesdato', None))
        kwargs['municipality_code'] = kwargs.pop('kommunekode', None)
        kwargs['street_code'] = kwargs.pop('vejkode', None)
        kwargs['house_number'] = kwargs.pop('husnr', None)
        kwargs['local_city_name'] = kwargs.pop('supplerendebynavn', None)
        kwargs['postal_code'] = kwargs.pop('postnr', None)
        kwargs['etrs89_east'] = kwargs.pop('etrs89koordinat_øst', None)
        kwargs['etrs89_north'] = kwargs.pop('etrs89koordinat_nord', None)
        kwargs['source'] = kwargs.pop('kilde', None)
        kwargs['house_number_source'] = kwargs.pop('husnummerkilde', None)
        kwargs['technical_standard'] = kwargs.pop('tekniskstandard', None)
        kwargs['text_orientation'] = kwargs.pop('tekstretning', None)
        kwargs['address_point_updated_datetime'] = parse_datetime(kwargs.pop('adressepunktændringsdato', None))
        kwargs['esdh_reference'] = kwargs.pop('esdhreference', None)
        kwargs['journal_number'] = kwargs.pop('journalnummer', None)
        kwargs['height'] = kwargs.pop('højde', None)
        kwargs['access_point_identifier'] = kwargs.pop('adgangspunktid', None)
        if kwargs['access_point_identifier'] is not None:
            kwargs['access_point_identifier'] = uuid.UUID(kwargs['access_point_identifier'])

        # The following fields are deprecated and are no longer updated
        kwargs.pop('ejerlavkode', None)
        kwargs.pop('matrikelnr', None)
        kwargs.pop('esrejendomsnr', None)
        super().__init__(**kwargs)

    @property
    def id(self) -> uuid.UUID:
        """Universal, unique identifier of the address.

        The identifier is stable trough our the life time of the address (like a CPR-number), no matter if the address
        change street name, house number, postal code or municipality code.

        :return: The identifer, e.g. ”0a3f507a-93e7-32b8-e044-0003ba298018” (id)
        """
        return super().get('id')

    @property
    def status(self) -> int:
        """The status of the access address.

        Status codes:
        - 1 indicates a valid address
        - 3 indicates a preliminary address

        :return: The status (status)
        """
        return super().get('status')

    @property
    def accuracy(self) -> str:
        """The accuracy of the access address

        A code that indicates the accuracy of the access address.

        Accuracy codes:
        - "A", the access address is absolute placed in a detailed base map. Typically an accuracy better than +/- 2 meters.
        - "B", the access address is calculated on a cadastral map. Typically centered in the cadastral and thus an accuracy worse than +/- 100 meters
        - "U", no access point

        :return: The accuracy (nøjagtighed)
        """
        return super().get('accuracy')

    @property
    def created_datetime(self) -> datetime.datetime:
        """The date and time for when the access address was registered in BBR.

        :return: The created datetime (oprettet)
        """
        return super().get('created_datetime')

    @property
    def updated_datetime(self) -> datetime.datetime:
        """The date and time for when the access address was last changed in BBR.

        :return: The updated datetime (ændret)
        """
        return super().get('updated_datetime')

    @property
    def commencement_datetime(self) -> datetime.datetime:
        """The date and time for when the access address was commencement

        :return: The commencement datetime (ikrafttrædelsesdato)
        """
        return super(self).get('commencement_datetime')

    @property
    def municipality_code(self) -> str:
        """The municipality code

        :return: The municipality code (kommunekode)
        """
        return super().get('municipality_code')

    @property
    def street_code(self) -> str:
        """Identification of a street.

        It is unique within the municipality. It is represented by four digits.

        Example: "0004" is "Abel Cathrines Gade" in the municipality of Compenhagen.

        :return: The identification code of the street (vejkode)
        """
        return super().get('street_code')

    @property
    def house_number(self) -> str:
        """The house number identifing the address from the other addresses with the same street name.

        The house number is a number between 1 and 999 and might have a capital letter A..Z and is determined in ascending order.

        :return: The hose number, e.g. "11", "12A" or "187B" (husnr)
        """
        return super(self).get('house_number')

    @property
    def local_city_name(self) -> str:
        """A supplementary city name.

        This is typically a local city name provided by the municipality. This is part of the official
        Indgår som en del af den officielle address description. Up to 34 characters.

        :return The local city name, e.g. Sønderholm (supplerendebynavn)
        """
        return super().get('local_city_name')

    @property
    def postal_code(self) -> str:
        """The postal code of where the address is located

        :return: A four digit postal code, e.g. "2400" for "København NV” (postnr)
        """
        return super().get('postal_code')

    @property
    def etrs89_east(self) -> float:
        """The eastern coordinate of the access address.

        The coordinate is provided in the coordination system UTM zone 32 and EUREF89/ETRS89

        :return: The eastern coordinate (etrs89koordinat_øst)
        """
        return super().get('etrs89_east')

    @property
    def etrs89_north(self) -> float:
        """The northern coordinate of the access address.

        The coordinate is provided in the coordination system UTM zone 32 and EUREF89/ETRS89

        :return: The northern coordinate (etrs89koordinat_nord)
        """
        return super().get('etrs89_north')

    @property
    def source(self):
        """A single character identifying the access address.

        "1": Created by a machine from a technical map
        "2": Created by a machine from the cadastral number's centroid
        "3": External reported by a consultant on be half of the municipality
        "4": External reported by the map office of the municipality
        "5": Created by the technical administration

        :return: The source (kilde)
        """
        return super().get('source')

    @property
    def house_number_source(self):
        """

        :return:
        """
        return super().get('house_number_source')

    @property
    def technical_standard(self):
        """

        :return:
        """
        return super().get('technical_standard')

    @property
    def text_orientation(self):
        """

        :return:
        """
        return super().get('text_orientation')

    @property
    def address_point_updated_datetime(self):
        """

        :return:
        """
        return super().get('address_point_updated_datetime')

    @property
    def esdh_reference(self):
        """

        :return:
        """
        return super().get('esdh_reference')

    @property
    def journal_number(self):
        """

        :return:
        """
        return super().get('journal_number')

    @property
    def height(self):
        """

        :return:
        """
        return super().get('height')

    @property
    def access_point_identifier(self):
        """

        :return:
        """
        return super().get('access_point_identifier')


class AccessAddressEvent(BaseResponse):
    """A sequence number

    A unique sequence number for an event in DAWA

    """
    def __init__(self, **kwargs) -> None:
        kwargs['sequence_number'] = int(kwargs['sekvensnummer'])
        kwargs['timestamp'] = parse_datetime(kwargs['tidspunkt'])
        kwargs['data'] = AccessAddressData(**kwargs['data'])
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
    def data(self) -> AccessAddressData:
        """The data

        :return: The data (data)
        """
        return super().get('data')
