from megalus.command.base import DockerBase
from megalus.core.message import notify
from megalus.core.utils import locale as _
from buzio import console


class Build(DockerBase):

    def run(self):

        console.section(_("Docker Build"), transform="center", full_width=True)

        # Get from name if informed
        name = ""
        container_id = None
        if self.arguments["<application>"]:
            container_id, name = self._get_application(container_base="build")
            if not name:
                return False

        # Login to ECR if used
        if self.project['use_ECR']:
            command = "aws ecr get-login --region {region}".format(
                region=self.profile['aws_region']
            )
            ret = self._run_command(
                task=command,
                run_stdout=True
            )
            if not ret:
                return False

        # Login to Docker Hub if used
        if self.project['use_Hub']:
            ret = self._run_command(
                task='docker info | grep "Username:"',
                get_stdout=True
            )
            if not ret or self.profile['docker_hub_user'] not in ret:
                command = "docker login -u {} -p {}".format(
                    self.profile['docker_hub_user'],
                    self.profile['docker_hub_pass']
                )
            ret = self._run_command(
                task=command,
                silent=True
            )
            if not ret:
                return False

        # Run all base images first - only once per image
        if self.arguments['--base-only'] or (
                not self.project['use_Hub'] and not self.project['use_ECR']):
            builted_images = []
            for application in self.project['dc_applications']:
                if application['base'] == "build":
                    if name and name != application['name']:
                        continue
                    if application['base_image_tag'] in builted_images:
                        continue
                    if application['build_base_first']:
                        command = "cd {} && docker build -t {}{} .".format(
                            application['base_path'],
                            " --no-cache " if self.arguments["--no-cache"] else "",
                            application['base_image_tag'])
                        ret = self._run_command(
                            title=_("Build base image for {}").format(
                                application['base_image_tag']), task=command)
                        if not ret:
                            return False
                        builted_images.append(application['base_image_tag'])

        # If build only bases, exit
        if self.arguments['--base-only']:
            notify(
                title="Docker Build",
                msg=_("Base image build completed.")
            )
            return True

        # Stop all containers
        ret = self._stop_all_containers()
        if not ret:
            return False

        # Build select application or all
        ret = self._run_command(
            title=_("Building {}").format(
                name if name else _("all containers")),
            task="cd {} && docker-compose build{}{}".format(
                self.project['dc_path'],
                "--no-cache" if self.arguments['--no-cache'] else "",
                " {}".format(name) if name else ""))

        # Stop and remove extra containers
        self._stop_all_containers()
        self._remove_extra_containers()

        if ret:
            notify(msg=_("Build operation complete for {}").format(
                name if name else _("all containers")
            )
            )
        else:
            notify(msg=_("An error occured during Docker build."))

        return ret
