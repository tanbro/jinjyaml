from typing import Any, Dict, Optional, Type

from .tagobject import JinjyamlObject, TLoadedObject
from .types import TJson

__all__ = ['jinjyaml_extract']


def jinjyaml_extract(
        obj: TLoadedObject,
        loader_class: Optional[Type] = None,
        context: Optional[Dict[str, Any]] = None
) -> TJson:
    """Render and parse recursively.

    It does:

    1. recursively search :class:`.JinjyamlObject` objects inside ``obj``.
    2. render the found :attr:`.JinjyamlObject.template` into strings.    
    3. parse the rendered strings into objects, using a `PyYAML Loader`.
    4. **in-place replace** :class:`.JinjyamlObject` objects with parsed data.

    .. attention::
        The ``obj`` parameter is modified by the function if :class:`.JinjyamlObject` objects in it.

    :type obj: dict, list, JinjyamlObject
    :param obj:
        What's loaded by `PyYAML`, with templates in it to render.

        It may be:

        * a :class:`dict` or :class:`list` object contains :class:`.JinjyamlObject` object(s)
        * a :class:`.JinjyamlObject` object

    :param loader_class:
        `PyYAML Loader`` class to parse the rendered string.

        .. note::
            The argument expects `PyYAML Loader` *class type*, **NOT** *instance*

    :type context: Dict[str, Any]
    :param context:
        variables name-value pairs for template rendering

    :return:
        Final extracted data
    """
    if context is None:
        context = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, JinjyamlObject):
                obj[k] = v.extract(loader_class, context)
            else:
                obj[k] = jinjyaml_extract(v, loader_class, context)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, JinjyamlObject):
                obj[i] = v.extract(loader_class, context)
            else:
                obj[i] = jinjyaml_extract(v, loader_class, context)
    elif isinstance(obj, JinjyamlObject):
        obj = obj.extract(loader_class, context)
    return obj
