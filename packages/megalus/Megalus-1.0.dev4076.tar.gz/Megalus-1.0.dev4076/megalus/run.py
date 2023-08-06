"""Megalus Tool.

For help type: 'meg help'

Usage:
    meg build [<application>] [--no-cache] [--base-only]
    meg change [<project>]
    meg create
    meg envs
    meg help
    meg profile
    meg project
    meg run [<application>] [<command>]
    meg stop [--force]
    meg up [<application>]

Options:
    --help          Show this text.

"""
import re
import sys
import os
import importlib
from docopt import docopt
from buzio import console
from tabulate import tabulate
from megalus import __version__
from megalus.core.utils import locale as _
from megalus.projects.settings import settings
from megalus.version import check_version


class Command():
    """Command class."""

    def __init__(self, settings=None):
        """Function: __init__.

        Summary: InsertHere
        Examples: InsertHere
        Attributes:
            @param (self):InsertHere
            @param (project):InsertHere
            @param (profile):InsertHere
        Returns: InsertHere
        """
        self.settings = settings

    def run(self, arguments):
        """Function: run.

        Summary: InsertHere
        Examples: InsertHere
        Attributes:
            @param (self):InsertHere
            @param (arguments):InsertHere
        Returns: InsertHere
        """
        self.arguments = arguments
        matches = re.finditer(r"(meg )(\w+)", __doc__)
        command = [
            m.group(2)
            for m in matches
            if self.arguments[m.group(2)]
        ][0]

        if command:
            if hasattr(self, "_{}".format(command)):
                function = getattr(self, "_{}".format(command))
                return function()
            else:
                module = importlib.import_module(
                    "megalus.command.{}".format(command))
                Klass = getattr(module, command.title())
                return Klass(
                    settings=self.settings,
                    arguments=self.arguments
                ).run()

    def _project(self):
        console.clear()
        return settings.show_project_config()

    def _profile(self):
        return settings.show_profile_config()

    def _change(self):
        return settings.change_project(name=self.arguments["<project>"])

    def _help(self):
        print("Help Placeholder")
        return True

    def _envs(self):
        env_list = [
            [obj, os.environ.get(obj, "")]
            for obj in self.settings.project['env_vars']
        ]
        console.section(_("Project Enviroment Variables"))
        print(tabulate(
            env_list,
            headers=[_("Variable"), _("Value")],
            tablefmt="presto"
        )
        )
        return True


def main():
    """Function: main.

    Main routine:
    1. Make several checks:
        - outdated version
        - has project
        - has profile
        - docker-compose.yml has modified
    2. Run edit_profile and/or edit_project if not settings
    3. Run apropriate command

    Return
    ------
    System Exit Code 0 or 1
    """
    # Show introduction
    console.box("Megalus v.{}".format(__version__))
    check_version()
    arguments = docopt(__doc__, version=__version__)

    # Show Help
    if arguments['help']:
        command = Command()
        command.run(arguments)
        sys.exit(0)
    else:
        console.info(
            _("For help type: 'meg help'"),
            use_prefix=False,
            theme="dark"
        )

    # Load data from files
    settings.load()

    # Check for Project
    if not settings.has_project:
        ret = console.confirm(
            "\n" + _("Project not found. Do you want create one?"),
            default=True)
        if ret:
            ret = settings.edit_project()
            sys.exit(ret)
    else:
        console.info(
            _("Current Project: {}").format(settings.project['name']),
            use_prefix=False
        )

    # If docker-compose.yml has changed
    if settings.has_project and settings.docker_compose_modified:
        ret = console.confirm(
            _("\nDocker-Compose file has changed. Do you want to update data"),
            theme="warning")
        if ret:
            settings.edit_project()
        else:
            settings.save_data()

    # Check for environment variables
    # except for profile/project commands
    if not arguments['project'] \
            and not arguments['profile'] \
            and not arguments['change']:
        if not settings.check_envs():
            sys.exit(1)

    # Check for profile
    if not settings.has_profile:
        ret = console.confirm(
            "\n" + _("Profile not found. Do you want create one?"),
            default=True)
        if ret:
            settings.edit_profile()
            sys.exit(0)

    # Run command if ready
    if settings.ready:
        command = Command(settings)
        ret = command.run(arguments)
    else:
        console.error(_("Configuration not ready"))
        ret = False

    if not ret:
        print('\n')
    else:
        print(_("\nOperation completed.\n"))

    sys.exit(ret)


if __name__ == "__main__":
    main()
