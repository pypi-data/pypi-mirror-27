import os
import pathlib
import re
from buzio import console
from megalus.command.base import DockerBase
from megalus.core.message import notify
from megalus.core.utils import locale as _


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
            path = application['path']
            if "$" in path:
                s = re.search("\${(\w+)}", application['path'])
                if s:
                    env = s.group(1)
                    name = os.environ.get(env)
                    path_list = [
                        part if "$" not in part else name
                        for part in application['path'].split("/")
                    ]
                    path = os.path.join(path_list)
                else:
                    console.error(
                        "Cant find path for {}".format(
                            application['name']))
                    return False
            if "." in path:
                list_path = os.path.join(self.project['dc_path'], path)
                path = os.path.abspath(list_path)

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
