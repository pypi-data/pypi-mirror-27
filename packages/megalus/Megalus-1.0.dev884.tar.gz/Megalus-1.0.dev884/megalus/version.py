"""Version package.

Checks version number for upgrades in PyPI
"""
import requests
from buzio import console
from distutils.version import LooseVersion
from megalus import __version__
from megalus.core.utils import locale as _

def versions():
    """Function: versions.

    Summary: Request all versions registered in PyPI
    Returns: list
    """
    url = "https://pypi.python.org/pypi/Megalus/json"
    data = None
    versions = None
    try:
        ret = requests.get(url, timeout=1)
        data = ret.json()
    except BaseException:
        pass
    if data:
        versions = list(data["releases"].keys())
        versions.sort(key=LooseVersion)
    return versions


def check_version():
    """Function: check_version.

    Summary: Compares actual version vs last known
    version in PyPI for upgrades
    Returns: Bool = true if updated
    """
    last_version = __version__
    version_data = versions()
    if version_data:
        last_version = version_data[-1]
    if LooseVersion(last_version) > LooseVersion(__version__) and \
            ("rc" not in last_version and
                "b" not in last_version and "dev" not in last_version):
        console.warning(
            _("You're running a outdated version.") + "\n" +
            _("Last Version: {}").format(last_version) + "\n"
        )
        return False
    else:
        return True

