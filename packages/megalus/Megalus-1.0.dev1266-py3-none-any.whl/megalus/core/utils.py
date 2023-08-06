"""Utils for packages."""
import gettext
import os
import subprocess
from buzio import console
from enum import Enum

args = {
    'domain': 'messages',
    'localedir': os.path.join('..', 'locale'),
    'fallback': True
}

t = gettext.translation(**args)
locale = t.gettext
_ = locale


class AutoEnum(Enum):
    """Base class for Auto Enums."""

    def __str__(self):
        """Magic string class.

        Return:
            string: name of the selected enum
        """
        return self.name

    def _generate_next_value_(name, start, count, last_values):
        """Generate next value for auto enum.

        Return:
            string: property name
        """
        return name

    @classmethod
    def listall(cls):
        """Return all object class enums.

        Return:
            object: every class member
        """
        return [
            member for name, member in cls.__members__.items()
        ]


def run_command(
        task,
        title=None,
        get_stdout=False,
        run_stdout=False,
        verbose=False,
        silent=False):
    if title:
        console.section(title)

    try:
        if run_stdout:
            if verbose:
                console.info(task, use_prefix=False)
            command = subprocess.check_output(task, shell=True)

            if not command:
                print(_('An error occur. Task aborted.'))
                return False

            if verbose:
                console.info(command, use_prefix=False)
            ret = subprocess.call(command, shell=True)

        elif get_stdout is True:
            if verbose:
                console.info(task, use_prefix=False)
            ret = subprocess.check_output(task, shell=True)
        else:
            if verbose:
                console.info(task, use_prefix=False)
            ret = subprocess.call(
                task if not silent else "{} 2>/dev/null 1>/dev/null".format(task),
                shell=True,
                stderr=subprocess.STDOUT
            )

        if ret != 0 and not get_stdout:
            return False
    except BaseException:
        return False

    return True if not get_stdout else ret.decode('utf-8')
