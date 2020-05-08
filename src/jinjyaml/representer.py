__all__ = ['JinjyamlRepresenter']


class JinjyamlRepresenter:
    """Representer for Jinja2 template tags

    When dumping an object into YAML string, the class represents :class:`.JinjyamlObject` object into template tag text

    Add the representer into YAML's dumper class as::

        representer = JinjyamlRepresenter('jinja2')  # No "!" here !!!
        yaml.add_representer(JinjyamlObject, representer)

    .. attention::

        - Custom tags in YAML should start with ``"!"``
        - But ``tag`` parameter should **NOT** start with ``"!"`` when creating :class:`JinjyamlRepresenter`
    """

    def __init__(self, tag: str):
        """

        :param str tag: YAML tag

        .. important::
            Custom YAML tags should start with ``"!"``, but do **NOT** put a ``"!"`` at the start of the parameter
        """
        self._tag = tag

    def __call__(self, dumper, data):
        return dumper.represent_scalar('!{}'.format(self._tag), data.source)
