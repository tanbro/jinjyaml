from typing import Dict, Any, Union, List

from .tagobject import JinjyamlObject

__all__ = ['jinjyaml_render']

TJson = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
TRenderObject = Union[TJson, JinjyamlObject]


def jinjyaml_render(
        obj: TRenderObject,
        loader_class=None,
        context: Dict[str, Any] = None
) -> TRenderObject:
    """recursive render function

    :param obj: :class:`dict` or :class:`list` object contains :class:`.JinjyamlObject` objects

    :param loader_class: ``PyYAML``'s Loader class.

        .. note:: Only ``yaml.Loader`` and ``yaml.FullLoader`` would load custom tags

    :param context: variables name-value pairs for :mod:`jinja2` template rendering
    :type context: Dict[str, Any]

    :return: The passed in ``obj`` with :class:`.JinjyamlObject` objects replaced

    it does:

    #. recursive find :class:`.JinjyamlObject` objects inside a :class:`dict` or a :class:`list` object.
    #. render the found :attr:`.JinjyamlObject.template` into texts.
    #. load the rendered texts into object, using a YAML loader.
    #. **in-place replace** :class:`.JinjyamlObject` objects with parsed objects.

    .. note:: The pass-in `obj` will be changed by the function if :class:`.JinjyamlObject` objects in it.
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
