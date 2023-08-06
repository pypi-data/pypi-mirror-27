#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""exceptions.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""


class DawaException(Exception):
    """The base exception

    The exception that all other exceptions inherit from.
    Follows the specification in https://dawa.aws.dk/generelt#fejlhaandtering

    DAWA exceptions is implemented in at https://github.com/DanmarksAdresser/Dawa/blob/master/apiSpecification/common/resourceImpl.js#L48

    Each error contains a title that describes the error in a human-readable manner in accommodation with the details
    provided by DAWA and the HTTP status code for the response that lead to this error

    :type title: str
    :type details: list | dict
    :type status_code: int
    """
    title = ''
    details = dict()
    status_code = 0

    def __init__(self, status_code: int, details=None):
        self.status_code = status_code

        if isinstance(details, dict):
            self.details = details
        elif isinstance(details, list):
            self.details = details


class UnknownException(DawaException):
    """Unknown error caught from DAWA.
    """
    title = 'Unknown error caught from DAWA.'


class UnknownContentType(DawaException):
    """Unknown content type.
    """
    title = 'Unknown content type.'


class JSONDecodeError(DawaException):
    """JSON decode error.
    """
    title = 'JSON decode error.'


class ResourcePathFormatError(DawaException):
    """The URI path was ill-formed.
    """
    title = 'The URI path was ill-formed.'


class QueryParameterFormatError(DawaException):
    """One or more query parameters was ill-formed.
    """
    title = 'One or more query parameters was ill-formed.'


class InternalServerError(DawaException):
    """Something unexpected happened inside the server.
    """
    title = 'Something unexpected happened inside the server.'


class InvalidRequestError(DawaException):
    """The request resulted in an invalid database query, probably due to bad query parameters.
    """
    title = 'The request resulted in an invalid database query, probably due to bad query parameters.'


class ResourceNotFoundError(DawaException):
    """The resource was not found.
    """
    title = 'The resource was not found.'
