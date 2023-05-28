from dataclasses import dataclass


@dataclass
class URLs:
    """
    login and logout urls for injecting into services.
    """

    login_url: str
    logout_url: str
