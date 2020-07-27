import io
import os
from typing import Optional
from configparser import ConfigParser

from paperswithcode import consts


class Config(object):
    """Configuration.

    Args:
        config_path (str, optional): Path to the configuration `ini` file. If
            the file is not provided, default configuration file
            `~/.paperswithcode/paperswithcode.ini` will be used.
        profile (str, optional): Selected profile from the `ini` file. Default:
            `default`.

    Attributes:
        config_path (str): Absolute path to the configuration `ini` file.
        profile (str): Selected profile.
        url (str): URL to the PapersWithCode website.
    """

    def __init__(
        self, config_path: Optional[str] = None, profile: str = "default"
    ):
        self.config_path = os.path.abspath(
            config_path or os.path.expanduser(consts.DEFAULT_CONFIG_PATH)
        )
        self.profile = profile
        if not os.path.isfile(self.config_path):
            data = {}
        else:
            cp = ConfigParser()
            cp.read(self.config_path)
            data = cp[self.profile] if cp.has_section(self.profile) else {}

        self.url = os.environ.get(
            "PAPERSWITHCODE_URL", data.get("url", consts.PAPERSWITHCODE_URL),
        )
        self.token = os.environ.get(
            "PAPERSWITHCODE_TOKEN", data.get("token", "")
        )

    def save(self):
        """Save the configuration file."""
        # Create config dir if it doesn't exist
        config_dir = os.path.dirname(self.config_path)
        os.makedirs(config_dir, exist_ok=True)

        cp = ConfigParser()
        # Read existing configuration if exists
        if os.path.isfile(self.config_path):
            cp.read(self.config_path)

        # Create profile if it doesn't exist
        if self.profile not in cp.sections():
            cp.add_section(self.profile)

        # Write the current configuration to the profile
        cp[self.profile]["token"] = self.token

        # Save configuration
        with io.open(self.config_path, "w") as f:
            cp.write(f)

    def __str__(self):
        return f"Config({self.config_path})"

    __repr__ = __str__
