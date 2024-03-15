import sys
from typing import Any, Mapping, MutableMapping, MutableSequence, Optional, Sequence

import jinja2
import yaml

from .data import Data

if sys.version_info < (3, 12):
    from ._yaml_types_backward import TYamlLoaderTypes
else:
    from ._yaml_types import TYamlLoaderTypes


__all__ = ["extract"]


def extract(
    obj: Any,
    loader_type: TYamlLoaderTypes,
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

              #. Recursively search inside the ``obj`` for :class:`.Data` objects.
              #. Render each found :meth:`.Data.source` as a :class:`jinja2.Template`.
              #. Parse the rendered string with the `PyYAML Loader` who loads ``obj``.
              #. Return the whole ``obj`` with :class:`.Data` objects replaced with corresponding parsed `Python` object.

            * A single :class:`.Data` object.

              In this case, the function does:

              #. Render :meth:`.Data.source` as a :class:`jinja2.Template`.
              #. Parse the rendered string with the `PyYAML Loader` who loads ``obj``.
              #. Return the parsed `Python` object.

            * Other scalar objects returned by a `PyYAML Loader`:

              In this case, the function directly returns ``obj`` with noting changed.

        loader_type: use this type of `PyYAML` Loader
        env: `Jinja2` environment for template rendering.
        context: Variables name-value pairs for `Jinja2` template rendering.

        inplace: Whether to make an in-place replace on :class:`.Data` objects inside the passed-in ``obj``.

            * When :data:`True`:
              In-place replace every :class:`.Data` object with corresponding parsed `Python` object inside the passed-in ``obj``.

            Tip:
                The ``obj`` must be a mutable :class:`dict` or :class:`list` like object in this case.

            Note:
                When the passed-in ``obj`` argument is an instance of :class:`.Data`, it **won't** be changed, even ``inplace`` was set :data:`True`.
                But if there was a :class:`dict` or :class:`list` object pared by YAML loader, which has cascade :class:`.Data` in it, the cascade part would be replaced.
                However, return value is just the pared result.

            * When :data:`False` (default):
              render and parse every :class:`.Data` object with corresponding parsed `Python` object, without modify the passed-in object.

    Returns:
        Final extracted `Python` object
    """  # noqa: E501
    if isinstance(obj, Data):
        tpl = env.from_string(obj.source) if env else jinja2.Template(obj.source)
        s = tpl.render(**(context or dict()))
        d = yaml.load(s, loader_type)
        return extract(d, loader_type, env, context, inplace)
    elif isinstance(obj, Mapping):
        if inplace:
            if not isinstance(obj, MutableMapping):
                raise ValueError(f"{obj!r} is not mutable")
            for k, v in obj.items():
                obj[k] = extract(v, loader_type, env, context, inplace)
        else:
            return {k: extract(v, loader_type, env, context, inplace) for k, v in obj.items()}
    elif isinstance(obj, Sequence) and not isinstance(obj, (bytearray, bytes, memoryview, str)):
        if inplace:
            if not isinstance(obj, MutableSequence):
                raise ValueError(f"{obj!r} is not mutable")
            for i, v in enumerate(obj):
                obj[i] = extract(v, loader_type, env, context, inplace)
        else:
            return [extract(m, loader_type, env, context, inplace) for m in obj]
    return obj
