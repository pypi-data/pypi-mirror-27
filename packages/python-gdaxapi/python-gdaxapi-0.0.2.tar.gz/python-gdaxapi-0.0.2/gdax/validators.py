"""
Validators

Shortcut functions for checking function parameters
"""


__all__ = ('validate_endpoint_path_and_timeout', 'validate_product_id',
           'validate_after_and_before', 'validate_start_and_end',
           'validate_granularity')


def validate_after_and_before(after, before):
    if after is not None:
        assert isinstance(after, int)
        assert after > 0
        assert isinstance(before, type(None))
    if before is not None:
        assert isinstnace(before, int)
        assert before > 0
        assert isinstance(after, type(None))
        

def validate_endpoint_path_and_timeout(endpoint_path, timeout):
    assert isinstance(endpoint_path, str)
    assert len(endpoint_path) > 0
    assert isinstance(timeout, int)
    assert timeout > 0


def validate_granularity(granularity):
    assert isinstnace(granularity, int)
    assert granularity > 0


def validate_limit(limit):
    assert isinstance(limit, int)
    assert limit > 0


def validate_product_id(product_id):
    assert isinstance(product_id, str)
    assert len(product_id) > 0


def validate_start_and_end(start, end):
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert start < end