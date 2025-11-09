# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os


def process_templates(colors: dict[str, str], paths: list[str]) -> list[str]:
    errors: list[str] = []

    for path in paths:
        template_file = os.path.expanduser(path)
        try:
            with open(template_file, "r") as file:
                template_content = file.read()
                for key, value in colors.items():
                    template_content = template_content.replace(
                        f"{{{{{key}}}}}", str(value))

            output_file = os.path.expanduser(
                template_file.replace("template.", ""))
            with open(output_file, "w") as file:
                file.write(template_content)

        except FileNotFoundError:
            errors.append(f"Could not find file: '{template_file}'")

    return errors
