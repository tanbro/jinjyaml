from typing import Any, Mapping, Sequence, Optional

import jinja2
import yaml

from .data import Data

__all__ = ['extract']


def extract(
        obj,
        env: Optional[jinja2.Environment] = None,
        context: Optional[Mapping[str, Any]] = None,
        inplace: bool = False
):
    """Recursively render and parse template tag objects in a YAML doc-tree.

    The ``obj`` parameter may be:

    * A mapping or sequence object returned by a `PyYAML Loader`.
      In this case, the function does:

        #. Recursively search :class:`.Data` objects inside ``obj``.
        #. Render :meth:`.Data.source` into a string with `Jinja2` .
        #. Parse the rendered string with the `PyYAML Loader` who loaded the ``obj`` .

        #. Do the render and parse:

            #. If ``inplace`` argument is ``True``:

               **In-place replace** each :class:`.Data` object with corresponding parsed `Python` object.

               In this case, ``obj`` should be mutable or it can not be changed.

            #. If ``inplace`` argument is ``False`` (default):

               render and parse each :class:`.Data` object with corresponding parsed `Python` object, without change the passed-in argument;

        #. Return the whole ``obj`` with :class:`.Data` objects replaced with corresponding rendered and parsed `Python` object.

    * A single :class:`.Data` object.
      In this case, the function does:

        1. Render :meth:`.Data.source` into a string with `Jinja2`.
        2. Parse the rendered string with the `PyYAML Loader` who loaded the ``obj``.
        3. Return the rendered and parsed `Python` object.

        .. note::
           When the passed-in `obj` argument is an instance of :class:`.Data`,
           it **won't** be changed even if set ``inplace`` to ``True``.
           However, return value is the pared object.

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

    :param bool inplace:
        In-place replace :class:`.Data` inside the passed-in ``obj`` argument's with parsed object.
        When ``True``, the ``obj`` should be mutable dict or list like object.

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
        s = template.render(**context)
        return yaml.load(s, obj.loader_type)
    elif isinstance(obj, Mapping):
        if inplace:
            for k, v in obj.items():
                obj[k] = extract(v, env, context, inplace=True)  # type: ignore
        else:
            return {k: extract(v, env, context, inplace=False) for k, v in obj.items()}
    elif isinstance(obj, Sequence) and not isinstance(obj, (bytearray, bytes, memoryview, str)):
        if inplace:
            for i, v in enumerate(obj):
                obj[i] = extract(v, env, context, inplace=True)  # type: ignore
        else:
            return [extract(m, env, context, inplace=False) for m in obj]
    return obj
