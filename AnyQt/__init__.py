import sys

__PREFERRED_API = None
__SELECTED_API = None
USED_API = None

def setpreferredapi(api):
    """
    Set the preferred Qt API.

    Note that QT_API environment variable (if set) will take precedence.
    """
    global __PREFERRED_API
    if __SELECTED_API is not None:
        raise RuntimeError("A Qt api {} was already selected"
                           .format(__SELECTED_API))
    __PREFERRED_API = api.lower()


def selectapi(api):
    """
    Select an Qt API to use.

    This can only be called once and before any of the Qt* modules are
    imported.
    """
    global __SELECTED_API, USED_API
    if __SELECTED_API is not None and __SELECTED_API.lower() != api.lower():
        raise RuntimeError("A Qt API {} was already selected"
                           .format(__SELECTED_API))
    elif __SELECTED_API is None:
        __SELECTED_API = api.lower()
        from . import _api
        USED_API = _api.USED_API


if sys.version_info < (3, 4):
    import imp as _imp
    def __islocatable(name):
        try:
            _imp.find_module(name)
        except ImportError:
            return False
        else:
            return True
else:
    import importlib.util as _importlibutil
    def __islocatable(name):
        try:
            return _importlibutil.find_spec(name) is not None
        except (ValueError, ImportError):
            return False


def availableapi():
    """
    Return a list of available Qt interfaces
    """
    search = ["PyQt5", "PyQt4", "PySide"]
    return [name for name in search if __islocatable(name)]
