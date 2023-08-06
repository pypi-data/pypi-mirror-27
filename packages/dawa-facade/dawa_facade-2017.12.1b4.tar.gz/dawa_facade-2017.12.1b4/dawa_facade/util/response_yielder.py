#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""response_yielder.py
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Martin Storgaard Dieu <ms@intramanager.com>, november 2017
"""
from ijson import ObjectBuilder
import dawa_facade.responses
import ijson.backends.yajl2_cffi as ijson
import requests


class DawaStream(object):
    def __init__(self, response: requests.Response):

        # Default to 65536 bytes chunks (this is what ijson uses)
        chunk_size = 65536  # TODO: Should this be tweaked?
        if response.headers.get('Transfer-Encoding', 'unknown') == 'chunked':
            # Transfer-Encoding is "chunked", then when chunk size is None we only read a chunk at a time from the
            # response. Observation: chunk_size is almost always None when calling DAWA
            chunk_size = None
        self.generator = response.iter_content(chunk_size=chunk_size)
        self.buffer = b''

    def read(self, size):
        if size == 0:
            # ijson calls read(0) to check if we are returning bytes
            return b''

        # Fill the buffer until the required size is reached
        try:
            while len(self.buffer) < size:
                self.buffer += next(self.generator)
        except StopIteration as e:
            if b'' == self.buffer:
                # There is nothing left to consume
                raise e
            if len(self.buffer) <= size:
                # Empty the buffer, otherwise do as usual
                content = self.buffer
                self.buffer = b''
                return content

        # Extract the desired size from the buffer and save the remaining data in the buffer
        content = self.buffer[:size]
        self.buffer = self.buffer[size:]
        return content


def yield_response(response: requests.Response):

    # Instantiate the JSON parser
    parser = ijson.parse(DawaStream(response))

    # Greatly inspired by https://github.com/isagalaev/ijson/blob/master/ijson/common.py#L130
    try:
        while True:
            current, event, value = next(parser)
            if event == 'start_map':
                builder = ObjectBuilder()
                end_event = event.replace('start', 'end')
                while event != end_event:
                    builder.event(event, value)
                    current, event, value = next(parser)
                # We now have a complete object in the list
                yield getattr(builder, 'value')
    except StopIteration:
        pass

