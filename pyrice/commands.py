# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess


def execute_commands(cmds: list[str]) -> list[str]:
    errors = []
    for cmd in cmds:
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            errors.append(str(res))
    return errors
