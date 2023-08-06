"""Settings package for Megalus."""
import os
from buzio import console
from megalus.core.utils import locale as _
from megalus.projects.data import DataMixin
from megalus.projects.profile import ProfileMixin
from megalus.projects.projects import ProjectMixin


class Setting(DataMixin, ProjectMixin, ProfileMixin):
    """Setting Class."""

    def __init__(self, *args, **kwargs):
        """Function: __init__.

        self.compose = data loaded from docker-compose.yml
        self.data = data loaded from ~/.megalus/megconfig.yml
        self.profile = Current User Data Dict
        self.project = Current Project Data Dict

        self.datapath = full path for megconfig.yml
        self.profilepath = full path for project user profile
        """
        self.compose = None
        self.data = {
            'config': {
                'current': None
            },
            'projects': {}
        }
        self.profile = None
        self.project = None

        self.datapath = None
        self.profilepath = None

    @property
    def ready(self):
        """Function: ready.

        Check if data is ready.

        Return
        ------
        Bool
        """
        return self.has_profile and self.has_project

    def check_envs(self):
        """Function: check_envs.

        Check if all environment variables
        listed on settings.project['env_vars']
        are settled in memory.

        Return
        ------
        Bool
        """
        ret = True
        env_data = None
        path = os.path.join(self.project['dc_path'], '.env')
        if os.path.isfile(path):
            console.info(_(".env file found."))
            with open(path, 'r') as file:
                env_data = file.read()
        for env in self.project['env_vars']:
            if not os.environ.get(env):
                if env_data and env in env_data:
                    continue
                console.error(
                    _("Define variable '{}' before start.").format(env))
                ret = False
        return ret


settings = Setting()
