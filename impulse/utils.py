import string

from hashids import Hashids

__all__ = [
    'generate_external_id',
]

hashids = Hashids(
    alphabet=string.ascii_lowercase,
    min_length=5,
    salt='foo'
)


def generate_external_id(internal_id):
    return hashids.encode(internal_id)
