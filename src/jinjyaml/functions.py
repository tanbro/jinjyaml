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
    """Recursively render and parse template tag objects in a YAML doc-tree.

    Args:

        obj: Object like list or dictionary contains :class:`.Data` instances.

            It may be:

            * A mapping or sequence object returned by `PyYAML Loader`.

              In this case, the function does:

              #. Recursively search inside ``obj`` for :class:`.Data` objects.
              #. Render :attr:`.Data.source` as string source of :class:`jinja2.Template` of each found :class:`.Data` object.
              #. Parse the rendered string with the `PyYAML Loader` who loads ``obj``.
              #. Return the whole ``obj`` with :class:`.Data` objects replaced with corresponding parsed `Python` object.

            * A single :class:`.Data` object.

              In this case, the function does:

              #. Render its :meth:`.Data.source` as string source of :class:`jinja2.Template`.
              #. Parse the rendered string with the `PyYAML Loader` who loads ``obj``.
              #. Return the parsed `Python` object.

            * Other scalar objects returned by a `PyYAML Loader`:

              In this case, the function directly returns ``obj`` with noting changed.

        loader_type: The `PyYAML Loader` who loads ``obj``
        env: `Jinja2` environment for template rendering.
        context: Variables name-value pairs for `Jinja2` template rendering.

        inplace: Whether to make an in-place replacement on :class:`.Data` objects inside ``obj``.

            * When :data:`True`:
              In-place replace every :class:`.Data` object with corresponding parsed `Python` object inside the passed-in ``obj``.
            * When :data:`False` (default):
              render and parse every :class:`.Data` object with corresponding parsed `Python` object, without modify the passed-in object.

            Tip:
                The ``obj`` must be a mutable :class:`dict` or :class:`list` like object if ``inplace`` is :data:`True`.

            Note:
                If the passed-in ``obj`` argument is an instance of :class:`.Data`, it **will not** be changed, even if ``inplace`` is set to :data:`True`.
                However, if there is a mutable :class:`dict` or :class:`list`-like object parsed by the YAML loader that contains nested :class:`.Data` objects, those nested parts will be replaced.
                The return value is always the parsed result.


    Returns:
        Final pared and extracted `Python` object
    """  # noqa: E501
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
