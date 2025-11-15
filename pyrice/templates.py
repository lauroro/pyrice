# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

# <%pyrice:key:oldvalue>
DIRECTIVE_RE = re.compile(
    r"<%pyrice:([a-zA-Z0-9_]+):([0-9a-fA-F]{6})>"
)


def process_templates(colors: dict[str, str], paths: list[str]) -> list[str]:
    """
    In-place inline template processing:
    Replaces occurrences of <oldvalue> in the next line of a directive,
    and updates the directive to reflect the new value.
    """

    errors: list[str] = []

    for path in paths:
        file_path = os.path.expanduser(path)

        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            errors.append(f"Could not find file: '{file_path}'")
            continue

        new_lines: list[str] = []

        i = 0
        while i < len(lines):
            line = lines[i]
            directives = list(DIRECTIVE_RE.finditer(line))

            if not directives:
                new_lines.append(line)
                i += 1
                continue

            # keep directive line, it will be updated
            original_line = line

            # check if next line exists
            if i + 1 >= len(lines):
                new_lines.append(line)
                break

            next_line = lines[i + 1]

            for m in directives:
                key = m.group(1)
                old = m.group(2)

                if key not in colors:
                    continue

                new = colors[key]

                # update next line
                next_line = next_line.replace(old, new)

                # update directive
                updated = f"<%pyrice:{key}:{new}>"
                original_line = original_line.replace(m.group(0), updated)

            new_lines.append(original_line)
            new_lines.append(next_line)

            i += 2

        with open(file_path, "w") as f:
            f.writelines(new_lines)

    return errors
