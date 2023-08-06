import re
import os
import json
from buzio import console
from megalus.core.utils import run_command
from megalus.core.utils import locale as _


class DockerBase():

    def __init__(self, settings, arguments):
        self.project = settings.project
        self.profile = settings.profile
        self.arguments = arguments

    def _run_command(self, *args, **kwargs):

        return run_command(*args, **kwargs)

    def _get_application(self, container_base=None):

        try:
            # Get container id and name for all running containers
            ret = self._run_command(
                get_stdout=True,
                task="docker ps"
            )
            if not ret:
                console.error(
                    _("Error during task execution. Process aborted."))
                return False, False

            ret = [
                (m.group(1), m.group(2))
                for m in re.finditer("(\w+) .+ (\w.+)", ret)
                if m.group(1) != "CONTAINER"
            ]

            running_services = [
                obj[1]
                for obj in ret
            ]
            raw_list = ret
            for app in self.project['dc_applications']:
                if app['name'] not in running_services:
                    raw_list.append(
                        (None, app['name'])
                    )

            # Filter by type, if informed
            container_list = []
            if container_base:
                for index, data in enumerate(raw_list):
                    data_type = [
                        obj['base']
                        for obj in self.project['dc_applications']
                        if obj['name'] == data[1]
                    ][0]
                    if data_type == container_base:
                        container_list.append(data)
            else:
                container_list = raw_list

            # Filter by name if informed
            if self.arguments['<application>']:
                container_list = [
                    obj
                    for obj in container_list
                    if self.arguments['<application>'] in obj[1]
                ]

            if not container_list:
                console.error(_("No valid container/application found."))
                return None, None

            # If one option remains return him
            if len(container_list) == 1:
                console.info(
                    "Found: {}".format(
                        container_list[0][1]),
                    use_prefix=False)
                return container_list[0]

            # Else choose from list
            else:
                choices = [
                    obj[1]
                    for obj in container_list
                ]
                ret = console.choose(choices)

                return [
                    obj
                    for obj in container_list
                    if obj[1] == ret
                ][0]
        except KeyboardInterrupt:
            return False, False

    def _stop_all_containers(self):
        ret = self._run_command(
            task="cd {} && docker-compose stop".format(
                self.project['dc_path']
            )
        )

        check = self._run_command(
            task="docker ps -q",
            get_stdout=True
        )

        if check:
            check = " ".join(check.split("\n"))
            ret = self._run_command(
                task="docker stop {}".format(check)
            )

        return ret

    def _remove_extra_containers(self):
        ret = self._run_command(
            task="docker ps -a",
            get_stdout=True
        )
        ret = [
            line.split(" ")[0]
            for line in ret.split("\n")
            if "__run__" in line
        ]
        if ret:
            os.system(
                "docker rm {}".format(" ".join(ret))
            )

    def _get_application_info(self, name):
        data = self._run_command(
            task="docker inspect {}".format(name),
            get_stdout=True
        )
        try:
            ret = json.loads(data)
            return ret[0]
        except BaseException:
            return None
