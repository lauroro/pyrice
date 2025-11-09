# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys


def parse_config_file(config_file: str) -> tuple[list[str], list[str]]:
    if not os.path.isfile(config_file):
        print(f"Config file not found: {config_file}")
        sys.exit(1)

    paths, cmds = [], []
    current_section = None

    with open(config_file, "r") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("paths:"):
                current_section = "paths"
                continue
            elif line.startswith("cmds:"):
                current_section = "cmds"
                continue

            if current_section == "paths" and line.startswith("-"):
                paths.append(line[1:].strip())
            elif current_section == "cmds" and line.startswith("-"):
                cmds.append(line[1:].strip())

    if not paths and not cmds:
        print(f"No valid sections found in config file: {config_file}")
        sys.exit(1)

    return paths, cmds
