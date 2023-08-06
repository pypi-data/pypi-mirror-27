import platform
from megalus.command.base import DockerBase
from megalus.core.utils import locale as _
from buzio import console


class Run(DockerBase):

    def run(self):
        console.section(_("Docker Run"), transform="center", full_width=True)

        # Get from name if informed
        name = ""
        container_id = None
        if self.arguments["<application>"]:
            container_id, name = self._get_application()
            if not name:
                return False

        if container_id:
            if self.arguments['<command>']:
                self._run_command(
                    task="docker exec -ti {container} {command}".format(
                        container=container_id,
                        command=self.arguments['<command>']
                    ),
                    verbose=True
                )
            else:
                self._run_service(name)
        else:
            if self.arguments['<command>']:
                self._run_command(
                    task="cd {path} && docker-compose "
                    "run --rm --service-ports {name} {command}".format(
                        path=self.project['dc_path'],
                        name=name,
                        command=self.arguments['<command>']),
                    verbose=True)
            else:
                self._run_service(name)

    def _run_service(self, name):
        data = self._get_application_info(name)
        if not data:
            console.error(_("Can't find data for {}".format(name)))
            return False
        if not data['State']['Running']:
            ret = self._run_command(
                task="cd {folder} && docker-compose up -d {name}".format(
                    folder=self.project['dc_path'],
                    name=name
                )
            )
            if not ret:
                console.error(_("Can't start {}".format(name)))
                return False

        service = [
            obj
            for obj in self.project['dc_applications']
            if obj['name'] == name
        ][0]
        if service['type'].name in ['Backend', 'Frontend', 'DevOps']:
            port = service['ports'][0]
            if ":" in port:
                url = "http://localhost:{}".format("".join(port.split(":")[0]))
                if platform.system().lower() != 'linux' \
                        and platform.system().lower() != 'windows':
                    command = "open -a " + \
                        self.project['browser'].get_command_name()
                else:
                    command = self.project['browser'].get_command_name
                open_command = command.format(url=url)
                self._run_command(
                    task=open_command,
                    verbose=True
                )
                return True
        console.warning('No startup command found for {}'.format(name))
