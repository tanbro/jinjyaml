from typing import Any, Dict, List, Optional, Type, Union

from .tagobject import JinjyamlObject

__all__ = ['jinjyaml_render']

TJson = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
TRenderObject = Union[TJson, JinjyamlObject]


def jinjyaml_render(
        obj: TRenderObject,
        loader_class: Type = None,
        context: Optional[Dict[str, Any]] = None
) -> TJson:
    """Recursive render function.

    it does:

    #. recursive find :class:`.JinjyamlObject` objects in ``obj`` parameter.
    #. render the found :attr:`.JinjyamlObject.template` into strings.
    #. parse the rendered strings into objects, using a YAML loader.
    #. **in-place replace** :class:`.JinjyamlObject` objects with parsed objects.

    .. attention::
        The ``obj`` parameter will be modified by the function if :class:`.JinjyamlObject` objects in it.

    :param obj: What's loaded by ``PyYAML``, with templates in it to render.

        It may be:

        * A :class:`dict` or :class:`list` contains :class:`.JinjyamlObject` object(s)
        * A :class:`.JinjyamlObject` object

    :type obj: dict, list, JinjyamlObject

    :param loader_class: ``PyYAML``'s ``Loader`` class to parse the rendered string.

    :param context: variables name-value pairs for template rendering
    :type context: Dict[str, Any]

    :return: The passed in ``obj`` with :class:`.JinjyamlObject` objects rendered and replaced
    """
    if context is None:
        context = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, JinjyamlObject):
                obj[k] = v.render(loader_class, context)
            else:
                obj[k] = jinjyaml_render(v, loader_class, context)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, JinjyamlObject):
                obj[i] = v.render(loader_class, context)
            else:
                obj[i] = jinjyaml_render(v, loader_class, context)
    elif isinstance(obj, JinjyamlObject):
        obj = obj.render(loader_class, context)
    return obj
