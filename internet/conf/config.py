"""
load configuration with validation.
"""

import dataclasses

from dynaconf import LazySettings, Validator


@dataclasses.dataclass()
class Database:
    """
    database dataclass configuration which is used in configuration
    dataclass.
    """

    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "radius"
    username: str = "opnsense"
    password: str = "opnsense%40123"


@dataclasses.dataclass
class Listen:
    """
    listen port and host for the http and workers configuration of sanic.
    """

    host: str = "0.0.0.0"
    port: int = 1378
    fast: bool = False
    workers: int = 1


@dataclasses.dataclass()
class Config:
    """
    configuration dataclass contains the application
    configuration.
    """

    listen: Listen = dataclasses.field(default_factory=Listen)
    database: Database = dataclasses.field(default_factory=Database)
    login_urls: dict[str, str] = dataclasses.field(
        default_factory=lambda: {
            "1": "https://login.aut.ac.ir/login",
        }
    )
    logout_urls: dict[str, str] = dataclasses.field(
        default_factory=lambda: {
            "1": "http://172.16.4.5:9090/logout",
        }
    )


def load() -> Config:
    """
    loads configuration with validation into Config.
    each new configuration must be validated and then set into config.
    """
    settings = LazySettings(
        settings_file=["config.toml"],
        envvar_prefix="INTERNET",
        nested_separator="__",
        validators=[
            Validator("database.host", is_type_of=(str), default="127.0.0.1"),
            Validator("database.port", is_type_of=(int), default=3306),
            Validator("database.database", is_type_of=(str), default="radius"),
            Validator("database.username", is_type_of=(str), default="opnsense"),
            Validator("database.password", is_type_of=(str), default="opnsense%40123"),
            Validator("listen.port", is_type_of=(int), default=1378),
            Validator("listen.host", is_type_of=(str), default="0.0.0.0"),
            Validator("listen.fast", is_type_of=(bool), default=False),
            Validator("listen.workers", is_type_of=(int), default=1),
            Validator(
                "login_urls",
                is_type_of=(dict),
                default={"1": "https://login.aut.ac.ir/login"},
            ),
            Validator(
                "logout_urls",
                is_type_of=(dict),
                default={"1": "http://172.16.4.5:9090/logout"},
            ),
        ],
    )

    cfg = Config()
    cfg.database.host = settings["database.host"]
    cfg.database.port = settings["database.port"]
    cfg.database.database = settings["database.database"]
    cfg.database.username = settings["database.username"]
    cfg.database.password = settings["database.password"]
    cfg.listen.port = settings["listen.port"]
    cfg.listen.host = settings["listen.host"]
    cfg.listen.workers = settings["listen.workers"]
    cfg.listen.fast = settings["listen.fast"]
    cfg.login_urls = settings["login_urls"]
    cfg.logout_urls = settings["logout_urls"]

    return cfg
