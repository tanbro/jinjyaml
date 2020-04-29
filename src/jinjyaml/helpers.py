from .tagobject import JinjyamlObject


def render_object(obj, loader_class=None, context=None):  # type (object, type, dict)->object
    """recursive render Jinja template object inside a dictionary or a list, then parse rendered text in YAML format

    1. recursive find jinja Template object in a dictionary or list object
    2. render the template into text
    3. load the rendered text in YAML format, parse them into object
    4. replace template with parsed object

    jinja2.Template in `obj` was replaced with YAML parsed object in place
    """
    if context is None:
        context = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, JinjyamlObject):
                obj[k] = v.render(loader_class, context)
            else:
                obj[k] = render_object(v, loader_class, context)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, JinjyamlObject):
                obj[i] = v.render(loader_class, context)
            else:
                obj[i] = render_object(v, loader_class, context)
    elif isinstance(obj, JinjyamlObject):
        obj = obj.render(loader_class, context)
    return obj
