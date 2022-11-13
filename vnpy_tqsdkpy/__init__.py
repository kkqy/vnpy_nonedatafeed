import importlib_metadata

from .tqsdk_datafeed import TqsdkpyDatafeed as Datafeed


try:
    __version__ = importlib_metadata.version("vnpy_tqsdk")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"
