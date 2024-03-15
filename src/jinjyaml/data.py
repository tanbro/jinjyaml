from dataclasses import dataclass

__all__ = ["Data"]


@dataclass(frozen=True)
class Data:
    """A `PyYAML` Custom tag stores string source of a :class:`jinja2.Template` object."""

    source: str
    """Source code of `jinja2.Template` object"""
