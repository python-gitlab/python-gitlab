from gitlab import cli
import pytest
import sys

PROJECT_ID = 9460322


def test_project_variable(capsys):
    key = "junk1"
    value1 = "car"
    value2 = "bus"

    with pytest.raises(SystemExit) as exit_exc:
        cmd_line = f"gitlab project-variable list --project-id {PROJECT_ID}"
        print("--->", cmd_line)
        sys.argv = cmd_line.split()
        cli.main()
    out, err = capsys.readouterr()

    if key not in out:
        with pytest.raises(SystemExit) as exit_exc:
            cmd_line = f"gitlab project-variable create --project-id {PROJECT_ID} --key {key} --value {value1}"
            print("--->", cmd_line)
            sys.argv = cmd_line.split()
            cli.main()
    out, err = capsys.readouterr()

    with pytest.raises(SystemExit) as exit_exc:
        cmd_line = f"gitlab project-variable get --project-id {PROJECT_ID} --key {key}"
        print("--->", cmd_line)
        sys.argv = cmd_line.split()
        cli.main()
    out, err = capsys.readouterr()

    with pytest.raises(SystemExit) as exit_exc:
        cmd_line = f"gitlab project-variable update --project-id {PROJECT_ID} --key {key} --value {value2}"
        print("--->", cmd_line)
        sys.argv = cmd_line.split()
        cli.main()
    out, err = capsys.readouterr()
    assert key in out
    assert value2 in out

    with pytest.raises(SystemExit) as exit_exc:
        cmd_line = f"gitlab project-variable list --project-id {PROJECT_ID}"
        print("--->", cmd_line)
        sys.argv = cmd_line.split()
        cli.main()
    out, _ = capsys.readouterr()

    if key in out:
        with pytest.raises(SystemExit) as exit_exc:
            cmd_line = f"gitlab project-variable delete --project-id {PROJECT_ID} --key {key}"
            print("--->", cmd_line)
            sys.argv = cmd_line.split()
            cli.main()
    out, _ = capsys.readouterr()

    pass