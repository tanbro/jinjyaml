from dataclasses import dataclass

__all__ = ["Data"]


@dataclass(frozen=True)
class Data:
    """A custom PyYAML tag that stores the string source of a :class:`jinja2.Template` object."""

    source: str
    """The source code of the `jinja2.Template` object."""
