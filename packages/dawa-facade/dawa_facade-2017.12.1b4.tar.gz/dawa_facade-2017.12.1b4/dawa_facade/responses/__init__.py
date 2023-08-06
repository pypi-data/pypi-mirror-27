#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__init__.py.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
import datetime


class BaseResponse(dict):
    """The base of all responses.

    All responses are stored as dictionaries due to ease of use.

    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


def parse_datetime(value) -> datetime.datetime:
        if value is None:
            return None
        try:
            value = int(value)
        except (ValueError, TypeError):
            value = str(value)

        if isinstance(value, int):
            if len(str(value)) == 13:
                # This is most likely from JavaScript new Date().getTime()
                value /= 1000.0
            return datetime.datetime.utcfromtimestamp(value)
        elif isinstance(value, str):
            # Remove any leading or trailing spaces
            value = value.strip().upper()
            if value[10].upper() == 'T':
                # 2016-09-01T19:21:56.934
                with_float = '%Y-%m-%dT%H:%M:%S.%f'
                without_float = '%Y-%m-%dT%H:%M:%S'
                if value.endswith('Z'):
                    # 2016-09-01T19:21:56.934Z
                    with_float += 'Z'
                    without_float += 'Z'
                try:
                    return datetime.datetime.strptime(value, with_float)
                except ValueError:
                    # Try without microseconds
                    return datetime.datetime.strptime(value, without_float)
            elif len(value) == 19:
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            else:
                raise ValueError('unknown datetime format')
        else:
            raise ValueError('unknown datetime format')
