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


@dataclasses.dataclass()
class Config:
    """
    configuration dataclass contains the application
    configuration.
    """
    database: Database = Database()
    login_url: str = "https://login.aut.ac.ir/login"
    logout_url: str = "http://172.16.4.5:9090/logout"


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
            Validator(
                "database.username", is_type_of=(str), default="opnsense"
            ),
            Validator(
                "database.password", is_type_of=(str), default="opnsense%40123"
            ),
            Validator(
                "login_url",
                is_type_of=(str),
                default="https://login.aut.ac.ir/login",
            ),
            Validator(
                "logout_url",
                is_type_of=(str),
                default="http://172.16.4.5:9090/logout",
            ),
        ],
    )

    cfg = Config()
    cfg.database.host = settings["database.host"]
    cfg.database.port = settings["database.port"]
    cfg.database.database = settings["database.database"]
    cfg.database.username = settings["database.username"]
    cfg.database.password = settings["database.password"]
    cfg.login_url = settings["login_url"]
    cfg.logout_url = settings["logout_url"]

    return cfg
