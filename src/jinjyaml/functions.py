from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Type, Union

import jinja2
import yaml

from .data import Data

if TYPE_CHECKING:  # pragma: no cover
    from yaml.cyaml import _CLoader
    from yaml.loader import _Loader


__all__ = ["extract"]


def extract(
    obj: Any,
    loader_type: Type[Union[_Loader, _CLoader]],
    env: Optional[jinja2.Environment] = None,
    context: Optional[Mapping[str, Any]] = None,
    inplace: bool = False,
) -> Any:
    """Recursively render and parse template tag objects in a YAML document tree.

    Args:
        obj: An object that may contain :class:`.Data` instances, such as a list or dictionary.

            It can be one of the following:

            * A mapping or sequence object returned by a `PyYAML Loader`.

                In this case, the function performs the following steps:

                1. Recursively searches inside ``obj`` for :class:`.Data` objects.
                2. Renders the :attr:`.Data.source` attribute as a string source for a :class:`jinja2.Template` for each found :class:`.Data` object.
                3. Parses the rendered string using the same `PyYAML Loader` that loaded ``obj``.
                4. Returns the entire ``obj`` with :class:`.Data` objects replaced by their corresponding parsed Python objects.

            * A single :class:`.Data` object.

                In this case, the function performs the following steps:

                1. Renders its :meth:`.Data.source` attribute as a string source for a :class:`jinja2.Template`.
                2. Parses the rendered string using the same `PyYAML Loader` that loaded ``obj``.
                3. Returns the parsed Python object.

            * Other scalar objects returned by a `PyYAML Loader`.

                In this case, the function directly returns ``obj`` without any changes.

        loader_type: The `PyYAML Loader` used to load ``obj``.
        env: The :class:`jinja2.Environment` for template rendering.
        context: A dictionary of variable name-value pairs for :mod:`jinja2` template rendering.

        inplace: Whether to perform an in-place replacement of :class:`.Data` objects within ``obj``.

            - When :data:`True`:
              Replaces every :class:`.Data` object with its corresponding parsed Python object within the passed-in ``obj``.

            - When :data:`False` (default):
              Renders and parses every :class:`.Data` object with its corresponding parsed Python object without modifying the passed-in object.

            Note:
                ``obj`` must be a mutable :class:`dict` or :class:`list`-like object if ``inplace`` is :data:`True`.

            Note:
                If the passed-in ``obj`` argument is an instance of :class:`.Data`, it will **not** be changed, even if ``inplace`` is set to :data:`True`.
                However, if there is a mutable :class:`dict` or :class:`list`-like object parsed by the YAML loader that contains nested :class:`.Data` objects, those nested parts will be replaced.
                The return value is always the parsed result.

    Returns:
        The final parsed and extracted Python object.
    """
    if isinstance(obj, Data):
        tpl = env.from_string(obj.source) if env else jinja2.Template(obj.source)
        s = tpl.render(**(context or dict()))
        d = yaml.load(s, loader_type)
        return extract(d, loader_type, env, context, inplace)
    elif isinstance(obj, Mapping):
        if inplace:
            if not isinstance(obj, MutableMapping):  # pragma: no cover
                raise ValueError(f"{obj!r} is not mutable")
            for k, v in obj.items():
                obj[k] = extract(v, loader_type, env, context, inplace)
        else:
            return {k: extract(v, loader_type, env, context, inplace) for k, v in obj.items()}
    elif isinstance(obj, Sequence) and not isinstance(obj, (bytearray, bytes, memoryview, str)):
        if inplace:
            if not isinstance(obj, MutableSequence):  # pragma: no cover
                raise ValueError(f"{obj!r} is not mutable")
            for i, v in enumerate(obj):
                obj[i] = extract(v, loader_type, env, context, inplace)
        else:
            return [extract(m, loader_type, env, context, inplace) for m in obj]
    return obj
