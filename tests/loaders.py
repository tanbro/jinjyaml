from warnings import warn

__all__ = ["LOADERS"]

from yaml import FullLoader, Loader, SafeLoader, UnsafeLoader

LOADERS = [SafeLoader, Loader, FullLoader, UnsafeLoader]
try:
    from yaml import CFullLoader, CLoader, CSafeLoader, CUnsafeLoader
except ImportError as err:
    warn(f"ImportError: {err}")
else:
    LOADERS += [CSafeLoader, CLoader, CFullLoader, CUnsafeLoader]
