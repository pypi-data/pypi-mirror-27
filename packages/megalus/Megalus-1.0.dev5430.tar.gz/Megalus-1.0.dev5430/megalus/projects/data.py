"""Data module.

Define Data class, which is used to manipulate
configuration files
"""
import glob
import os
import yaml
import getpass
import uuid
from buzio import console
from megalus.core.utils import locale as _
from megalus.core.utils import run_command


class DataMixin():
    """Manipulate datafiles.

    megconfig.yml - Main configuration and Projects data
    docker-compose.yml - Data from docker compose
    <project slug>_<$USER>.yml - Project User profiles
    """

    @property
    def docker_compose_modified(self):
        """Property: docker_compose_modified.

        Check if docker-compose.yml has changed

        Return
        ------
        Bool
        """
        path = os.path.join(self.project['dc_path'], "docker-compose.yml")
        try:
            timestamp = os.path.getmtime(path)
        except IOError:
            console.error(_("Cannot read docker-compose.yml"))
            return True
        dc_check = self.project['dc_timestamp'] != timestamp

        path = os.path.join(
            self.project['dc_path'], "docker-compose.override.yml")
        if os.path.isfile(path):
            try:
                timestamp = os.path.getmtime(path)
            except IOError:
                console.error(_("Cannot read docker-compose.override.yml"))
                return True
            if self.project.get('dco_timestamp', False):
                dco_check = self.project['dco_timestamp'] != timestamp
            else:
                dco_check = True
        else:
            dco_check = False
        return dc_check or dco_check

    def load(self):
        """Function: load.

        Try read project and user data from disk,
        creating folder and file if not exists.
        """
        basepath = os.path.expanduser("~")
        self.path = os.path.join(basepath, ".megalus")
        self.datapath = os.path.join(self.path, "megconfig.yml")

        # Create path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # Load data
        if os.path.isfile(self.datapath):
            with open(self.datapath, 'r') as file:
                self.data = yaml.load(file.read())

        # Load current project
        if self.data['projects'] and self.data['config']['current']:
            self.project = \
                self.data['projects'][self.data['config']['current']]

        # Load user
        if self.project:
            self.profilepath = self._get_profile_path()
            if os.path.isfile(self.profilepath):
                with open(self.profilepath, 'r') as file:
                    self.profile = yaml.load(file.read())

    def save_data(self):
        """Function: save.

        Save contents in megconfig.yml
        from settings.data and settings.project
        """
        if self.project:
            project_key = self._get_project_id()
            path = os.path.join(self.project['dc_path'], 'docker-compose.yml')
            self.project['dc_timestamp'] = os.path.getmtime(path)
            path = os.path.join(
                self.project['dc_path'], 'docker-compose.override.yml')
            if os.path.isfile(path):
                self.project['dco_timestamp'] = os.path.getmtime(path)
            self.data['projects'][project_key] = self.project
            if not self.data['config']['current']:
                self.data['config']['current'] = project_key
        with open(self.datapath, 'w') as file:
            yaml.dump(self.data, file)

    def delete_project(self):
        """Function: delete_project.

        Delete current project:
        1. clear settings.project and settings.profile
        2. Remove project from megconfig.yml
        3. Remove all project user profiles from disk
        """
        ret = console.confirm(
            _("Do you really want to delete project"),
            default=False)
        if ret:
            project_key = self._get_project_id()
            self.data['projects'].pop(project_key)
            remaining_projects = [proj for proj in self.data['projects']]
            if remaining_projects:
                new_proj = console.choose(remaining_projects)
            else:
                new_proj = None
            self.data['config']['current'] = new_proj
            with open(self.datapath, 'w') as file:
                yaml.dump(self.data, file)
            for file in glob.glob(
                    os.path.join(self.path, "{}*.yml".format(project_key))):
                os.remove(file)
            self.project = None
            self.profile = None

    def _validate_yaml(self, filepath):
        """Check if path is valid for yaml file.

        Parameter
        ---------
        filepath : path
            Absolute path for yaml file
        Return
        ------
        Boolean
            True if file can be read.
        """
        long_path = os.path.join(
            os.path.expanduser("~") if "~" in filepath else "",
            filepath.replace("~", ""),
            "docker-compose.yml"
            if "docker-compose" not in filepath else ""
        )
        print(_("Reading {}").format(long_path))
        ret = run_command(
            task="cd {} && docker-compose config 1>/dev/null".format(filepath),
            get_stdout=True
        )
        if ret:
            console.error("Found errors in docker-compose configuration:")
            console.info(ret)
            return False
        try:
            with open(long_path, 'r') as file:
                yaml.load(file.read())
        except Exception as e:
            console.error(e)
            return False
        return True

    def _get_project_id(self):
        """Get Project Id.

        Return or generate unique ID.

        Return
        ------
        String: uuid4
        """
        if self.project.get('unique_id', False):
            return self.project['unique_id']
        else:
            return str(uuid.uuid4()).replace("-", "")[:10]

    def _get_profile_path(self):
        config_file = "{}_{}.yml".format(
            self.data['config']['current'],
            getpass.getuser()
        )
        return os.path.join(self.path, config_file)
