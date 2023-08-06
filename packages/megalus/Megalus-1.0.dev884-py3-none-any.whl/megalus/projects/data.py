"""Data module.

Define Data class, which is used to manipulate
configuration files
"""
import glob
import os
import yaml
import getpass
from buzio import console, formatStr
from megalus.core.utils import locale as _


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
        timestamp = os.path.getmtime(self.project['dc_path'])
        return self.project['dc_timestamp'] != timestamp

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
            project_key = self._get_project_slug()
            self.project['dc_timestamp'] = os.path.getmtime(
                self.project['dc_path'])
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
            project_key = self._get_project_slug()
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
        try:
            with open(long_path, 'r') as file:
                yaml.load(file.read())
        except Exception as e:
            console.error(e)
            return False
        return True

    def _get_project_slug(self):
        """Slugify project name.

        - Convert " " to "_"
        - Lowercase all characters
        - Remove accents

        Return
        ------

        String: slugify version of string
        """
        return formatStr.slugify(self.project['name'])

    def _get_profile_path(self):
        config_file = "{}_{}.yml".format(
            self.data['config']['current'],
            getpass.getuser()
        )
        return os.path.join(self.path, config_file)
