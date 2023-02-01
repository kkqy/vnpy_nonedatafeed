import importlib_metadata

from .none_datafeed import NoneDatafeed as Datafeed


try:
    __version__ = importlib_metadata.version("vnpy_nonedatafeed")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"
