"""
load configuration with validation.
"""

import dataclasses

from dynaconf import LazySettings, Validator


@dataclasses.dataclass()
class Database:
    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "radius"
    username: str = "opnsense"
    password: str = "opnsense@123"


@dataclasses.dataclass()
class Config:
    database: Database = Database()
    login_url: str = "https://login.aut.ac.ir/login"


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
                "database.password", is_type_of=(str), default="opnsense@123"
            ),
            Validator(
                "login_url",
                is_type_of=(str),
                default="https://login.aut.ac.ir/login",
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

    return cfg
