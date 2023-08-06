from megalus.command.base import DockerBase
from megalus.core.utils import locale as _
from buzio import console


class Up(DockerBase):

    def run(self):
        console.section(_("Docker Up"), transform="center", full_width=True)

        # Get from name if informed
        name = ""
        container_id = None
        if self.arguments["<application>"]:
            container_id, name = self._get_application()
            if not name:
                return False

        if name:
            if container_id:
                ret = self._run_command(
                    task='docker stop {}'.format(container_id)
                )
            ret = self._run_command(
                task="cd {folder} && docker-compose up -d {name}".format(
                    folder=self.project['dc_path'],
                    name=name
                )
            )
        else:
            # Stop all containers
            ret = self._stop_all_containers()
            if not ret:
                return False
            ret = self._run_command(
                task="cd {folder} && docker-compose up".format(
                    folder=self.project['dc_path']
                )
            )
        return True
