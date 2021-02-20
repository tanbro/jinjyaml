from typing import (Any, Mapping, MutableMapping, MutableSequence, Optional,
                    Type)

from .data import Data

__all__ = ['extract']


def extract(
        obj,
        loader_class: Optional[Type] = None,
        context: Optional[Mapping[str, Any]] = None
):
    """Render and parse recursively.

    It does:

    1. Recursively search :class:`.Data` objects inside ``obj``.
    2. Call :meth:`.Data.extract` of each found object
    3. **In-place replace** each :class:`.Data` object with corresponding extracted data.

    .. attention::
        The ``obj`` parameter is modified in the function if any :class:`.Data` object in it.

    :type obj: dict, list, Data
    :param obj:
        What parsed by `PyYAML Loader`.

        It may be:

        * a :class:`dict` or :class:`list` object contains :class:`.Data` object(s)
        * a :class:`.Data` object

    :param loader_class:
        `PyYAML Loader` class to parse the rendered string.

        .. note::
            The argument expects `PyYAML Loader` *class type*, **NOT** *instance*

    :type context: Dict[str, Any]
    :param context:
        variables name-value pairs for `Jinja2` template rendering

    :return:
        Final extracted data
    """
    if context is None:
        context = dict()
    if isinstance(obj, Data):
        obj = obj.extract(loader_class, context)
    elif isinstance(obj, MutableMapping):
        for k, v in obj.items():
            obj[k] = extract(v, loader_class, context)
    elif isinstance(obj, MutableSequence) and not isinstance(obj, (bytearray, bytes, str)):
        for i, v in enumerate(obj):
            obj[i] = extract(v, loader_class, context)
    return obj
