from src.main import Main

import os


def test_env_vars():
    # Given
    env_vars = [
        dict(key="HOST", value="0.0.0.0"),
        dict(key="TOKEN", value="testtoken"),
        dict(key="DATABASE", value="testdb"),
        dict(key="TICKETS", value="10"),
        dict(key="T_MAX", value="78"),
        dict(key="T_MIN", value="12"),
    ]

    # When
    main = Main(lambda: load_test_vars(env_vars))

    # Then
    assert main.HOST == "0.0.0.0"
    assert main.TOKEN == "testtoken"
    assert main.DATABASE == "testdb"
    assert main.TICKETS == "10"
    assert main.T_MAX == "78"
    assert main.T_MIN == "12"

def load_test_vars(env_vars):
    for env_var in env_vars:
        os.environ[env_var["key"]] = env_var["value"]
