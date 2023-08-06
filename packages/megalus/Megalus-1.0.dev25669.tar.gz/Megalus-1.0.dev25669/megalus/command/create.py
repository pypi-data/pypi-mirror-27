import os
import pathlib
import re
from buzio import console
from megalus.command.base import DockerBase
from megalus.core.message import notify
from megalus.core.utils import locale as _
from megalus.core.utils import get_path


class Create(DockerBase):

    def run(self, delete_data=False):

        console.clear()
        console.section(
            _("Create {} Project".format(self.project['name'])),
            transform="center",
            full_width=True)

        ret = console.confirm()
        if not ret:
            return False

        # Stop all containers
        self._stop_all_containers()

        if delete_data or console.confirm(
                "Delete all Docker data before cloning"):
            self._run_command(
                title=_("Excluding docker data"),
                task="cd {folder} && docker-compose down".format(
                    folder=self.project['dc_path'])
            )

        for application in self.project['dc_applications']:
            if application['base'] == "image":
                continue

            console.section(_("Application: {}".format(application['name'])))
            path = get_path(application['path'], self.project['dc_path'])

            console.info(_("Working directory: {}".format(path)),
                         use_prefix=False)
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            if not os.listdir(path):
                ret = self._run_command(
                    title=_("Cloning {}".format(application['repo'])),
                    task="cd {} && git clone {} .".format(
                        path,
                        application['repo']
                    )
                )
            else:
                console.info(
                    _("Dir exists. Skipping...".format(path)))
