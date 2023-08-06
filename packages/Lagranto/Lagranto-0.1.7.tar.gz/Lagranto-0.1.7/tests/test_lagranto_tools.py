from lagranto.tools import run_cmd, LagrantoException


def test_error_in_run_cmd():
    try:
        run_cmd('echo ERROR', cmd_header='')
    except LagrantoException as err:
        error = "\n    cd '.'\n     echo ERROR\n    ERROR\n"
        assert err.args[0] == error
