"""Profile module."""
import yaml
from buzio import console
from tabulate import tabulate
from megalus.core.utils import locale as _


class ProfileMixin():
    """Setting Class."""

    @property
    def has_profile(self):
        """Property: has_profile.

        Check if user data exists.

        Return
        ------
        Bool
        """
        return self.profile is not None

    def edit_profile(self):
        """Function: edit_profile.

        Ask for profile fields to
        populate settings.profile
        """
        base_profile = {
            "aws_key": "",
            "aws_secret": "",
            "aws_region": "",
            "aws_account": "",
            "slack_url": "",
            "slack_channel": "",
            "slack_icon": "",
            "slack_user": "",
            "docker_hub_user": "",
            "docker_hub_pass": ""
        }
        if not self.profile:
            self.profile = base_profile
        else:
            for key in base_profile:
                if self.profile.get(key, None) is None:
                    self.profile[key] = base_profile[key]
        helptxt = {
            "aws_key":
                _("AWS Key"),
            "aws_secret": _("AWS Secret"),
            "aws_region": _("AWS Region"),
            "aws_account": _("AWS account number"),
            "slack_url": _("Slack Webhook URL"),
            "slack_channel": _("Slack Channel"),
            "slack_icon": _("Slack Icon"),
            "slack_user": _("Slack Username"),
            "docker_hub_pass": _("Docker Registry Password"),
            "docker_hub_user": _("Docker Registry User")
        }
        key_list = sorted([key for key in self.profile])
        console.section(
            _("{} Profile").format(_("Create")
                                   if not self.profile else _("Edit")),
            full_width=True
        )
        try:
            for key in key_list:
                if "aws" in key and not self.project['use_aws']:
                    continue
                if "slack" in key and not self.project['use_slack']:
                    continue
                if "hub" in key and not self.project['use_Hub']:
                    continue
                else:
                    question = helptxt[key]
                self.profile[key] = console.ask(
                    question,
                    default=self.profile[key] if self.profile[key] else None,
                    required=True
                )
        except KeyboardInterrupt:
            return False

        self.show_profile_config()

    def show_profile_config(self):
        """Function: show_profile_config.

        Show profile fields and ask for options
        Edit, Save or Exit
        """
        console.section(_("User Configuration"))
        key_list = sorted([key for key in self.profile])
        table_data = [
            [key, self.profile[key]]
            for key in key_list
            if self.profile[key]
        ]
        print(tabulate(
            table_data,
            headers=[_("Key"), _("Value")],
            tablefmt="presto"
        ))
        print("\n")
        try:
            ret = console.select(
                [
                    _('Edit'),
                    _("Save and Exit"),
                    _("Exit")
                ],
                default=1
            )
            if ret == 0:
                self.edit_profile()
            elif ret == 1:
                self.save_profile()
                console.info(_("Data successfully saved."))
                return True
            else:
                self.profile = None
                return False
        except KeyboardInterrupt:
            return False

    def save_profile(self):
        """Function: save_profile.

        Save settings.profile data
        in separate file on disk.

        Filename is <project slug>_<$USER>.yml
        """
        if self.profile:
            if not self.profilepath:
                self.profilepath = self._get_profile_path()
            with open(self.profilepath, 'w') as file:
                yaml.dump(self.profile, file)
