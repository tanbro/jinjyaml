from dataclasses import dataclass

__all__ = ["Representer"]


@dataclass
class Representer:
    """Representer for :class:`jinja2.Template` tags.

    When dumping an object into YAML string,
    convert :class:`.Data` to string.

    Add the representer to `PyYAML Dumper` as below::

        representer = jinjyaml.Representer("j2")  # No "!" here !!!
        yaml.add_representer(Node, representer)

    """  # noqa: E501

    tag: str
    """YAML tag name for include statement

    Attention:
        Custom YAML tag's name starts with ``"!"``.
        But we **MUST NOT** put a ``"!"`` at the beginning here,
        because :func:`yaml.add_representer` will add the symbol itself.
    """

    def __call__(self, dumper, data):
        return dumper.represent_scalar(f"!{self.tag}", data.source)
