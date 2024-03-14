from typing import Type

__all__ = ["Data"]


class Data:
    """A `PyYAML` Custom tag represents a `jinja2.Template` object."""

    def __init__(
        self,
        source: str,
        loader_type: Type,
    ):
        self._source = source
        self._loader_type = loader_type

    @property
    def source(self) -> str:
        """Source code to make `jinja2.Template`"""
        return self._source

    @property
    def loader_type(self) -> Type:
        """`PyYAML Loader` class parsing the tag object."""
        return self._loader_type
