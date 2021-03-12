from typing import Optional, Type

__all__ = ['Data']


class Data:
    """A `PyYAML` Custom tag represents a `Jinja2` template object.
    """

    def __init__(self,
                 source: str,
                 loader_type: Optional[Type] = None,
                 ):
        self._source = source
        self._loader_type = loader_type

    @property
    def source(self) -> str:
        """Source code to make `Jinja2` template.

        :rtype: str
        """
        return self._source

    @property
    def loader_type(self) -> Optional[Type]:
        """`PyYAML Loader` class parsing the tag object.

        :rtype: Type
        """
        return self._loader_type
