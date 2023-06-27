from warnings import warn

import yaml

__all__ = ["LOADERS"]

LOADERS = []

if "3.12" <= yaml.__version__ < "4.0":
    from yaml import SafeLoader, Loader

    LOADERS = [SafeLoader, Loader]
    try:
        from yaml import CBaseLoader, CSafeLoader, CLoader
    except ImportError as err:
        warn(Warning(err))
    else:
        LOADERS += [CBaseLoader, CSafeLoader, CLoader]
elif "5.0" <= yaml.__version__ < "7.0":
    from yaml import SafeLoader, Loader, FullLoader, UnsafeLoader

    LOADERS = [SafeLoader, Loader, FullLoader, UnsafeLoader]
    try:
        from yaml import CSafeLoader, CLoader, CFullLoader, CUnsafeLoader
    except ImportError as err:
        warn("{}".format(err))
    else:
        LOADERS += [CSafeLoader, CLoader, CFullLoader, CUnsafeLoader]
else:
    raise NotImplementedError(f"Un-supported PyYAML version: {yaml.__version__}")
