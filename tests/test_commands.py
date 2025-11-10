# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
from pyrice import commands


# ---------- TEST: execute_commands ----------
def test_execute_commands_success(monkeypatch):
    # all commands will succeed
    def mock_run(cmd, shell):
        class Result:
            returncode = 0
        return Result()
    monkeypatch.setattr(subprocess, "run", mock_run)

    cmds = ["echo ok", "ls"]
    errors = commands.execute_commands(cmds)
    assert errors == []


def test_execute_commands_failure(monkeypatch):
    # when a command fails, error should be collected
    def mock_run(cmd, shell):
        class Result:
            returncode = 1
            def __str__(self): return f"<Failed {cmd}>"
        return Result()
    monkeypatch.setattr(subprocess, "run", mock_run)

    cmds = ["badcmd"]
    errors = commands.execute_commands(cmds)
    assert len(errors) == 1
    assert "badcmd" in errors[0]


def test_execute_commands_mixed(monkeypatch):
    # case where some commands succeed and some fail
    def mock_run(cmd, shell):
        class Result:
            def __init__(self, code): self.returncode = code
            def __str__(self): return f"<{cmd} rc={self.returncode}>"
        return Result(0 if "good" in cmd else 1)
    monkeypatch.setattr(subprocess, "run", mock_run)

    cmds = ["good1", "bad1", "good2", "bad2"]
    errors = commands.execute_commands(cmds)
    assert len(errors) == 2
    assert all("bad" in e for e in errors)
