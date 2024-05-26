from dataclasses import dataclass


@dataclass
class URLs:
    """
    login and logout urls for injecting into services.
    """

    login_urls: dict[str, str]
    logout_urls: dict[str, str]
