import platform
from megalus.core.utils import run_command
from megalus.core.utils import locale as _
from buzio import formatStr, console


def notify(msg, title=None):
    if not title:
        title = "Megalus"
    if platform.system().lower() == 'linux':  # Linux
        run_command(
            task='notify-send -i gsd-xrandr {title} {msg}'.format(
                title='"{}"'.format(formatStr.unitext(title)),
                msg='"{}"'.format(formatStr.unitext(msg))
            )
        )
    elif platform.system().lower() == "windows" \
            and platform.version()[:2] == "10":  # Windows 10

        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, msg)
        except ImportError:
            console.warning(
                _("Win10toast not found. For receive windows "
                    "notifications from Megalus please install using "
                    "'pip install win10toast'")
            )

    else:  # Mac
        run_command(
            task="osascript -e 'display notification "
            "{msg} with title {title}'".format(
                title='"{}"'.format(
                    formatStr.unitext(title)),
                msg='"{}"'.format(
                    formatStr.unitext(msg))
            )
        )
