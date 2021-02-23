from typing import Any, Mapping, MutableMapping, MutableSequence, Optional

import jinja2
import yaml

from .data import Data

__all__ = ['extract']


def extract(
    obj,
    env: Optional[jinja2.Environment] = None,
    context: Optional[Mapping[str, Any]] = None
):
    """Recursively render and parse template tag objects in a YAML doc-tree.


    The ``obj`` parameter may be:

    * A mapping or sequence object returned by a `PyYAML Loader`.
      In this case, the function does:

        1. Recursively search :class:`.Data` objects inside ``obj``.
        2. Render :meth:`.Data.source` into a string with `Jinja2`.
        3. Parse the rendered string with the `PyYAML Loader` who loaded the ``obj``.
        4. **In-place replace** each :class:`.Data` object with corresponding parsed `Python` object.
        5. Return the whole ``obj`` with :class:`.Data` objects replaced with corresponding rendered and parsed `Python` object.

        .. attention::
            ``obj`` is modified if any :class:`.Data` object in it.

    * A single :class:`.Data` object.
      In this case, the function does:

        1. Render :meth:`.Data.source` into a string with `Jinja2`.
        2. Parse the rendered string with the `PyYAML Loader` who loaded the ``obj``.
        3. Return the rendered and parsed `Python` object.

    * Other scalar objects returned by a `PyYAML Loader`.
      In this case, the function returns ``obj`` with noting changed.

    :type obj: dict, list, Data
    :param obj:
        What already parsed by `PyYAML Loader`.

    :param jinja2.Environment env:
        Environment for `Jinja2` template rendering.

    :type context: Mapping[str, Any]
    :param context:
        Variables name-value pairs for `Jinja2` template rendering.

    :return:
        Final extracted `Python` object
    """
    if isinstance(obj, Data):
        if env is None:
            template = jinja2.Template(obj.source)
        else:
            template = env.from_string(obj.source)
        if context is None:
            context = dict()
        txt = template.render(**context)
        obj = yaml.load(txt, obj.loader_type)
    elif isinstance(obj, MutableMapping):
        for k, v in obj.items():
            obj[k] = extract(v, env, context)
    elif isinstance(obj, MutableSequence) and not isinstance(obj, (bytearray, bytes, str)):
        for i, v in enumerate(obj):
            obj[i] = extract(v, env, context)
    return obj
