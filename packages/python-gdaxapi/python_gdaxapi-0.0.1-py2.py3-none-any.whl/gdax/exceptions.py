"""
Exceptions

Custom exceptions for issues with API calls
"""


__all__ = ('PaginationException', 'ExcessivePaginationErrors',
           'ExcessivePaginationRequests')


class PaginationException(Exception):
    pass


class ExcessivePaginationErrors(PaginationException):
    pass


class ExcessivePaginationRequests(PaginationException):
    pass