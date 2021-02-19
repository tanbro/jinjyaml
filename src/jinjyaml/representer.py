__all__ = ['JinjyamlRepresenter']


class JinjyamlRepresenter:
    """Representer for Jinja2 template tags.

    When dumping an object into YAML string,
    convert :class:`.JinjyamlObject` to string.

    Add the representer into ``PyYAML``'s ``Dumper`` as below::

        representer = JinjyamlRepresenter('jinja2')  # No "!" here !!!
        yaml.add_representer(JinjyamlObject, representer)

    .. attention::

        Custom YAML tags starts by ``"!"``.

        But,  we **SHOULD NOT** put a ``"!"`` at the begin of ``tag``
        -- the function ``yaml.add_representer`` will add the symbol itself.
    """

    def __init__(self, tag: str):
        """
        :param str tag: YAML tag
        """
        self._tag = tag

    def __call__(self, dumper, data):
        return dumper.represent_scalar('!{}'.format(self._tag), data.source)
