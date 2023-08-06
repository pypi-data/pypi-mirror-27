import platform
from megalus.command.base import DockerBase
from megalus.core.utils import locale as _
from buzio import console


class Stop(DockerBase):

    def run(self):
        console.section(_("Docker Stop"), transform="center", full_width=True)

        ret = self._stop_all_containers()
        if not ret:
            return False
        self._remove_extra_containers()
        if self.arguments['--force']:
            ret = self._run_command(
                task="docker ps -q"
            )
            if ret:
                console.warning(_("Force stop frozen containers"))
                self._run_command(
                    task="docker update --restart=no $(docker ps -q)"
                )
                if platform.system().lower() == "linux":
                    self._run_command(
                        task="systemctl restart docker"
                    )
                else:
                    console.success("Please restart Docker to complete operation.")
        return True

