__all__ = ['Representer']


class Representer:
    """Representer for `Jinja2` template tags.

    When dumping an object into YAML string,
    convert :class:`.Data` to string.

    Add the representer to `PyYAML Dumper` as below::

        representer = jinjyaml.Representer('j2')  # No "!" here !!!
        yaml.add_representer(Node, representer)

    .. attention::

        Custom YAML tags start with ``"!"``.

        But, here we **SHOULD NOT** put a ``"!"`` at the begining of ``tag``
        -- ``yaml.add_representer`` will add the symbol itself.
    """

    def __init__(self, tag: str):
        """
        :param str tag: YAML tag
        """
        self._tag = tag

    def __call__(self, dumper, data):
        return dumper.represent_scalar('!{}'.format(self._tag), data.source)
