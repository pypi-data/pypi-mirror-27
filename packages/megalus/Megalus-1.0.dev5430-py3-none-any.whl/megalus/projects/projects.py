"""Project module."""
import os
import re
import yaml
from buzio import console, formatStr
from enum import auto
from tabulate import tabulate
from megalus.core.utils import locale as _
from megalus.core.utils import AutoEnum, get_path, run_command


class AppType(AutoEnum):
    """Enum for Application Types."""

    Backend = auto()
    Frontend = auto()
    Database = auto()
    Cache = auto()
    Broker = auto()
    Worker = auto()
    DevOps = auto()


class Browser(AutoEnum):
    """Enum for Browsers."""

    Chrome = auto()
    Firefox = auto()
    Edge = auto()
    Safari = auto()

    def get_command_name(self):
        if self.name == "Chrome":
            data = "google-chrome {url}"
        elif self.name == "Firefox":
            data = "firefox {url}"
        elif self.name == "Edge":
            data = "start microsoft-edge:{url}"
        else:
            data = "Safari {url}"
        return data

class VCS(AutoEnum):
    """Enum for VCS services."""

    GitHub = auto()
    Bitbucket = auto()

    def get_data(self):
        """Function: get_data.

        Return API endpoints for selected CVS. If you choose
        'other' no information was given.

        Return
        ------
        dict or None
        """
        if self.name == "Github":
            data = {
                "vcs_base_url": "https://{token}@github.com/{name}",
                "vcs_api_url": "https://api.github.com",
                "vcs_repository_url": "repos/{name}/{repo}/commits/{sha}",
                "vcs_pull_request_url": "/repos/{name}/{repo}/pulls"
            }
        elif self.name == "Bitbucket":
            data = {
                "vcs_base_url": "https://{token}@bitbucket.org/{name}/",
                "vcs_api_url": "https://api.bitbucket.org/",
                "vcs_repository_url":
                "2.0/repositories/{name}/{repo}/commit/{sha}/statuses",
                "vcs_pull_request_url":
                "2.0/repositories/{name}/{repo}/pullrequests/"}
        else:
            data = None
        return data


class ProjectMixin():
    """Setting Class."""

    @property
    def has_project(self):
        """Property: has_project.

        Check if project data exists.

        Return
        ------
        Bool
        """
        return self.project is not None

    def edit_project(self):
        """Function: edit_project.

        Loads docker-compose.yml and other fields
        to populate settings.project
        """
        base_project = {
            "dc_path": "",
            "dc_version": "",
            "dc_timestamp": "",
            "name": "",
            "env_vars": [],
            "use_vpn": False,
            "dc_applications": [],
            "git_token": "",
            "use_aws": False,
            "use_slack": False,
            "use_ECR": False,
            "use_Hub": False,
            "browser": Browser.Chrome
        }
        try:
            if not self.project:
                title = _("Create new Project")
                self.project = base_project
            else:
                title = _("Edit Project")
                for key in base_project:
                    if self.project.get(key, None) is None:
                        self.project[key] = base_project[key]
            self.helptxt = {
                "dc_path": _("Absolute path to docker-compose.yml"),
                "name": _("Project Name"),
                "env_vars": _(
                    "List all mandatory Environment "
                    "Variables (use , to separate them)"),
                "use_vpn": _("Use VPN for deploy/build?"),
                "git_token": _("Your Github Personal Token "
                               "or Bitbucket App Password"),
                "use_aws": _("Use AWS"),
                "use_slack": _("Use Slack"),
                "use_ECR": _("Use Amazon ECR for docker images"),
                "use_Hub": _("Use Docker Hub for docker images"),
                "browser": _("Browser for open frontend/backend applications")}

            console.clear()
            console.section(title, full_width=True, transform="center")

            console.section(_("1. Answer the following questions"
                              " for configure project."))

            for config_key in sorted([k for k in self.project]):

                if config_key == "browser":
                    self.project[config_key] = console.choose(
                        Browser.listall(),
                        question=self.helptxt.get(
                            config_key,
                            config_key),
                        default=self.project['browser'])
                    print("\n")
                    continue

                # Ask after reading docker-compose
                if config_key == "env_vars":
                    continue

                # Ignore docker-compose fields
                elif "dc_" in config_key:
                    continue
                else:
                    # Get boolean fields
                    if isinstance(self.project[config_key], bool):
                        self.project[config_key] = console.confirm(
                            self.helptxt.get(config_key, config_key),
                            default=self.project[config_key]
                            if self.project[config_key] is not None else None
                        )

                    # Get list fields
                    elif isinstance(self.project[config_key], list):
                        ret = console.ask(
                            self.helptxt.get(config_key, config_key),
                            required=True,
                            default=self.project[config_key]
                            if self.project[config_key] else None
                        )
                        if isinstance(ret, list):
                            self.project[config_key] = ret
                        else:
                            self.project[config_key] = ret.split(",")

                    # Get and validate name field
                    elif config_key == "name":
                        self.project[config_key] = console.ask(
                            self.helptxt.get(config_key, config_key),
                            required=True, validator=self._check_name,
                            default=self.project['name']
                            if self.project['name'] else None)

                    # Other fields
                    else:
                        self.project[config_key] = console.ask(
                            self.helptxt.get(config_key, config_key),
                            required=True,
                            default=self.project[config_key]
                            if self.project[config_key] else None)

            # Parse data from compose
            self.get_data_from_compose()

            # Check for environment variables
            console.section(_("3. Define environment variables"))
            default_list = self.project["env_vars"] \
                if self.project["env_vars"] else self._get_env_vars()
            ret = console.ask(
                self.helptxt.get("env_vars", "env_vars"),
                required=True,
                default=default_list
            )
            if isinstance(ret, list):
                self.project["env_vars"] = ret
            else:
                self.project["env_vars"] = ret.split(",")
        except KeyboardInterrupt:
            return False

        # Show config and options
        self.show_project_config()

    def get_data_from_compose(self):
        """function: get_data_from_compose.

        Parse data from Docker-Compose file
        iterating each service for asking specific
        fields for them.
        """
        # Find Docker-compose.yml
        console.section(_("2. Answer the following questions"
                          " for configure containers."))
        self.project['dc_path'] = console.ask(
            self.helptxt['dc_path'],
            validator=self._validate_yaml,
            default=self.project['dc_path']
            if self.project['dc_path'] else None
        )

        # Load data from yaml
        dcpath = os.path.join(
            os.path.expanduser("~")
            if "~" in self.project['dc_path'] else "",
            self.project['dc_path'].replace("~", ""),
            "docker-compose.yml")
        with open(dcpath, 'r') as file:
            self.raw_data = file.read()
            self.compose = yaml.load(self.raw_data)

        # Load docker-compose.override.yml if exists
        dcpath = os.path.join(
            os.path.expanduser("~")
            if "~" in self.project['dc_path'] else "",
            self.project['dc_path'].replace("~", ""),
            "docker-compose.override.yml")
        if os.path.isfile(dcpath):
            console.info("Found: docker-compose.override.yml")
            with open(dcpath, 'r') as file:
                self.override = yaml.load(file.read())
            for key in self.override:
                self._load_data_from_override(self.override, self.compose, key)

        # Parse data from Docker-Compose.yml
        self.project['dc_version'] = self.compose['version']
        self.project['dc_timestamp'] = os.path.getmtime(
            self.project['dc_path'])
        old_list = self.project['dc_applications']
        self.project['dc_applications'] = []

        for key in self.compose['services']:
            console.section(key, theme="info")

            # Container Name and Base
            data = self.compose['services'][key]
            name = data['container_name'] \
                if 'container_name' in data else key
            container_base = 'build' if 'build' in data else 'image'

            # Container Type
            old_data = self.get_application_data(name, old_list)
            container_type = console.choose(
                choices=AppType.listall(),
                question=_("Select Type for: '{}'").format(key),
                default=old_data.get('type',
                                     self._get_application_default(key))
                if old_data else self._get_application_default(key))

            # Container Links and Ports
            links = data.get('links', [])
            ports = data.get('ports', [])

            # Ask for Ngrok Tunnel
            use_ngrok = console.confirm(
                "Create Ngrok tunnel",
                default=old_data.get(
                    'ngrok', False) if old_data else False
            )

            # Options for 'build' base containers
            if container_base == "build":
                old_data = self.get_application_data(name, old_list)
                path = data.get('build')
                if isinstance(path, dict):
                    path = path.get('context')
                repo = console.ask(
                    _("Repository URL"),
                    required=True,
                    default=old_data.get(
                        'repo', self._find_repo(path, self.project['dc_path']))
                    if old_data else self._find_repo(path, self.project['dc_path'])
                )
                base_first = console.confirm(
                    _("This service needs to build (not download) base image first"
                        " using another dockerfile?"),
                    default=old_data['build_base_first']
                    if old_data else False
                )

                if base_first:
                    base_path = console.ask(
                        _("Path to base image Dockerfile"),
                        required=True,
                        validator=self._find_dockerfile,
                        default=old_data['base_path'] if old_data else None
                    )
                    base_image_tag = console.ask(
                        _("Base image tag (use format 'name:tag')"),
                        required=True,
                        validator=self._check_image_name,
                        default=old_data['base_image_tag']
                        if old_data else None)
                else:
                    base_path = None
                    base_image_tag = None
                if data.get('build', {}).get('dockerfile', None):
                    dockerfile_dev = data['build']['dockerfile']
                else:
                    dockerfile_dev = "Dockerfile"
                dockerfile_stage = console.ask(
                    _("Dockerfile name for stage"),
                    default=dockerfile_dev)
                dockerfile_deploy = console.ask(
                    _("Dockerfile name for deploy"),
                    default=dockerfile_dev)
                if data.get('build', {}).get('context', None):
                    container_path = data['build']['context']
                else:
                    container_path = data['build']

                self.project['dc_applications'].append(
                    {
                        'name': name,
                        'base': container_base,
                        'type': container_type,
                        'links': links,
                        'ports': ports,
                        'repo': repo,
                        'path': container_path,
                        'ngrok': use_ngrok,
                        'build_base_first': base_first,
                        'base_path': base_path,
                        'base_image_tag': base_image_tag,
                        'dockerfile': {
                            'dev': dockerfile_dev,
                            'stage': dockerfile_stage,
                            'deploy': dockerfile_deploy
                        }
                    }
                )
            else:
                self.project['dc_applications'].append(
                    {
                        'name': name,
                        'base': container_base,
                        'type': container_type,
                        'links': links,
                        'ports': ports
                    }
                )

    def show_project_config(self):
        """Function: show_project_config.

        Show project fields using tabulate
        and ask for options:
        Add, Edit, Save, Delete Project or Exit
        """
        console.section(
            _("Project Configuration: {}").format(
                self.project['name']),
            full_width=True)
        console.info(
            _("Docker-Compose path: {}\n").format(
                self.project['dc_path']), use_prefix=False)
        table_data = []
        key_list = sorted([key for key in self.project])
        for key in key_list:
            if "dc_" in key and key != "dc_applications":
                continue
            data = self.project[key]
            if isinstance(data, list):
                if key == "dc_applications":
                    for i, app_dict in enumerate(data):
                        for x, app_config in enumerate(app_dict):
                            if app_dict[app_config] is None:
                                continue
                            if isinstance(app_dict[app_config], list):
                                for z, listn in enumerate(
                                        app_dict[app_config]):
                                    table_data.append([
                                        key if x == 0 else "",
                                        app_dict['name'] if x == 0 else "",
                                        app_config if z == 0 else "",
                                        listn
                                    ])
                            elif isinstance(app_dict[app_config], dict):
                                for z, listn in enumerate(
                                        app_dict[app_config]):
                                    table_data.append([
                                        key if x == 0 else "",
                                        app_dict['name'] if x == 0 else "",
                                        app_config if z == 0 else "",
                                        "{}: {}".format(
                                            listn, app_dict[app_config][listn])
                                    ])
                            elif app_config == "base_path" \
                                    and app_dict[app_config]:
                                last_one = os.path.split(
                                    app_dict[app_config])[-1]

                                table_data.append([
                                    key if x == 0 and i == 0 else "",
                                    app_dict['name'] if x == 0 else "",
                                    app_config,
                                    "..." + last_one
                                ])
                            else:
                                table_data.append([
                                    key if x == 0 and i == 0 else "",
                                    app_dict['name'] if x == 0 else "",
                                    app_config,
                                    app_dict[app_config]
                                ])
                elif isinstance(data, list):
                    for i, item in enumerate(data):
                        table_data.append([
                            key if i == 0 else "",
                            item
                        ])
                else:
                    for i, item in enumerate(data):
                        table_data.append([
                            key if i == 0 else "",
                            formatStr(item)
                        ])
            else:
                table_data.append(
                    [key, data]
                )
        print(tabulate(
            table_data,
            headers=[_("Key"), _("Value"), _("Key"), _("Value")],
            tablefmt="presto"
        ))

        print('\n')
        try:
            ret = console.select(
                [
                    _("Add"),
                    _("Edit"),
                    _("Delete"),
                    _("Save and Exit"),
                    _("Exit")
                ],
                default=3
            )
            if ret == 0:
                self.project = None
                self.edit_project()
            elif ret == 1:
                self.edit_project()
            elif ret == 2:
                self.delete_project()
                console.success(_("Project deleted."))
                return True
            elif ret == 3:
                self.save_data()
                console.success(_("Project saved."))
                return True
            else:
                return True
        except KeyboardInterrupt:
            return False

    def change_project(self, name=None):
        """Function: change_project.

        Change current project.
        """
        if name:
            project_list = [
                self.data['projects'][key]['name']
                for key in self.data['projects']
                if name in self.data['projects'][key]['name'].lower()
            ]
        else:
            project_list = [
                self.data['projects'][key]['name']
                for key in self.data['projects']
            ]
        if not project_list:
            console.error(_("No Project Found."))
            ret = None
        elif len(project_list) == 1:
            ret = project_list[0]
        else:
            console.section(_("Change current project"))
            try:
                ret = console.choose(
                    sorted([key for key in project_list])
                )
            except KeyboardInterrupt:
                console.error(_("Operation interrupted."))
                return False
        if not ret:
            return False
        ret = self._get_project_id()
        changed = True if ret != self.data['config']['current'] else False
        self.data['config']['current'] = ret
        self.save_data()
        if changed:
            console.success(_("Current Project changed to {}").format(ret))
        else:
            console.info(_("Current project not changed"))

    def _check_name(self, name):
        names_list = [
            key for key in self.data['projects']
        ]
        name = formatStr.slugify(name)
        return name not in names_list

    def _get_application_default(self, key):
        if re.search("cache", key):
            return AppType.Cache
        elif re.search("redis|rabbit|broker", key):
            return AppType.Broker
        elif re.search("postgres|db|sql|database|mongo", key):
            return AppType.Database
        elif re.search("api|back|django|pyramid|java|flask|chalice", key):
            return AppType.Backend
        elif re.search("front|spa|angular|react|vue|riot", key):
            return AppType.Frontend
        elif re.search("worker|celery|beat|flower", key):
            return AppType.Worker
        elif re.search("ngrok|pgadmin|sentry|kibana|logstash|traefik", key):
            return AppType.DevOps
        else:
            return None

    def _find_dockerfile(self, path):
        testpath = os.path.join(path, 'Dockerfile')
        ret = os.path.isfile(testpath)
        if not ret:
            console.error(
                _("Dockerfile not found on: {}").format(testpath))
        return ret

    def _get_env_vars(self):

        data = re.finditer("\${(\w+)}", self.raw_data)

        env_var_list = set([
            m.group(1)
            for m in data
        ])

        return list(env_var_list)

    def get_application_data(self, name, search_list=None):
        """Summary.

        Parameters
        ----------
        name : TYPE
            Description
        search_list : None, optional
            Description

        Return
        ------
        TYPE
            Description
        """
        if not search_list:
            search_list = self.project['dc_applications']
        ret = [
            app_data
            for app_data in search_list
            if app_data['name'] == name
        ]
        return ret[0] if ret else None

    def _check_image_name(self, name):
        m = re.search(r"(\w+:\w+)", name)
        return True if m else False

    def _find_repo(self, path, dc_path):
        path = get_path(path, dc_path)
        if os.path.isdir(path):
            cd_command = "cd {}".format(path)
            repo = run_command(
                task=cd_command + " && git remote -v | head -n 1 | awk '{print $2}'",
                get_stdout=True
            )
            if repo:
                repo = repo.replace('\n', '')
        return repo if repo else ""

    def _load_data_from_override(self, source, target, key):
        """Append override data in self.compose.

            Example Compose
            ---------------
            core:
                build:
                    context: ../core
                image: core
                networks:
                    - backend
                ports:
                 - "8080:80"

            Example override
            ----------------
            core:
                build:
                    dockerfile: Docker_dev
                depends_on:
                    - api
                command: bash -c "python manage.py runserver 0.0.0.0"
                ports:
                    - "9000:80"

            Final Result
            ------------
            core:
                build:
                    context: ../core
                    dockerfile: Docker_dev
                depends_on:
                    - api
                image: core
                command: bash -c "python manage.py runserver 0.0.0.0"
                networks:
                    - backend
                ports:
                 - "9000:80"

        """
        if target.get(key, None):
            if isinstance(source[key], dict):
                for k in source[key]:
                    self._load_data_from_override(
                        source=source[key],
                        target=target[key],
                        key=k
                    )
            else:
                target[key] = source[key]
        else:
            target[key] = source[key]
