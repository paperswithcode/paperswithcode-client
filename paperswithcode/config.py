from pathlib import Path

from tea_client.config import TeaClientConfig
from tea_console.config import TeaConsoleConfig, ConfigField


class Config(TeaConsoleConfig, TeaClientConfig):
    ENTRIES = {
        **TeaConsoleConfig.ENTRIES,
        "server_url": ConfigField(section="server", option="url"),
        "api_version": ConfigField(
            section="server", option="api_version", type=int
        ),
        "token_access": ConfigField(section="auth", option="token_access"),
        "token_refresh": ConfigField(section="auth", option="token_refresh"),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (
            Path("~").expanduser() / ".paperswithcode"
        ).absolute()
        TeaClientConfig.__init__(
            self, server_url="https://paperswithcode.com", api_version=1
        )
        TeaConsoleConfig.__init__(
            self, config_file=self.config_dir / "paperswithcode.ini"
        )


config = Config()
