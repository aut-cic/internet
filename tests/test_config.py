import pytest

from internet.conf import load


def test_loading() -> None:
    cfg = load()

    assert cfg.database.host == "127.0.0.1"
    assert cfg.database.port == 3306
    assert cfg.database.database == "radius"


def test_loading_with_env(monkeypatch: pytest.MonkeyPatch) -> None:
    # monkeypatch (rather than a bare os.environ assignment) so the override is
    # undone afterwards and cannot leak into whatever test runs next.
    monkeypatch.setenv("INTERNET_DATABASE__PORT", "3307")
    monkeypatch.setenv("INTERNET_DATABASE__HOST", "localhost")

    cfg = load()

    assert cfg.database.host == "localhost"
    assert cfg.database.port == 3307
    assert cfg.database.database == "radius"


def test_defaults_restored_after_env_override() -> None:
    # Guards the leak the previous test used to cause.
    cfg = load()

    assert cfg.database.host == "127.0.0.1"
    assert cfg.database.port == 3306


def test_login_and_logout_urls_have_default_site() -> None:
    cfg = load()

    assert cfg.login_urls["1"].startswith("http")
    assert cfg.logout_urls["1"].startswith("http")
