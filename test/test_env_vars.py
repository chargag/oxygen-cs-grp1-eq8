from src.main import Main

import os


def test_env_vars():
    # Given
    env_vars = [
        dict(key="HOST", value="0.0.0.0"),
        dict(key="TOKEN", value="testtoken"),
        dict(key="DB_HOST", value="localhost"),
        dict(key="DB_NAME", value="dbtest"),
        dict(key="DB_PORT", value="32"),
        dict(key="DB_USER", value="user"),
        dict(key="DB_PASSWORD", value="password"),
        dict(key="TICKS", value="10"),
        dict(key="T_MAX", value="78"),
        dict(key="T_MIN", value="12"),
    ]

    # When
    main = Main(lambda: load_test_vars(env_vars))

    # Then
    assert main.HOST == "0.0.0.0"
    assert main.TOKEN == "testtoken"
    assert main.DB_HOST == "localhost"
    assert main.DB_NAME == "dbtest"
    assert main.DB_PORT == "32"
    assert main.DB_USER == "user"
    assert main.DB_PASSWORD == "password"
    assert main.TICKS == "10"
    assert main.T_MAX == "78"
    assert main.T_MIN == "12"


def load_test_vars(env_vars):
    for env_var in env_vars:
        os.environ[env_var["key"]] = env_var["value"]
