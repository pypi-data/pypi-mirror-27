# language=rst
"""
Recursively freeze mutable dicts, sets and lists.

Example usage::

    import config_loader

    MY_FROZEN_DICT = config_loader.freeze(my_mutable_dict)

"""

from collections import abc
import types
import numbers


def freeze(thing):
    # language=rst
    """Creates a frozen copy of ``thing``.

    :param thing:
    :type thing: bool or None or str or numbers.Number or dict or list or set
    :returns: a frozen copy of ``thing``, using the following transformations:

        -   `dict` → `types.MappingProxyType`
        -   `set` → `frozenset`
        -   `list` → `tuple`

    """
    # ¡¡¡ Ordering matters in the following if-chain !!!
    # abc.Set inherits abc.Collection, so it must be matched first.
    if (
        thing is None or
        isinstance(thing, bool) or
        isinstance(thing, numbers.Number) or
        isinstance(thing, str)
    ):
        return thing
    if isinstance(thing, abc.Mapping):
        return types.MappingProxyType({key: freeze(thing[key]) for key in thing})
    if isinstance(thing, abc.Set):
        return frozenset({freeze(value) for value in thing})
    if isinstance(thing, abc.Collection):
        return tuple([freeze(value) for value in thing])
    raise TypeError("Can't freeze object of type %s: %s" %
                    (type(thing), thing))
