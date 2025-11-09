# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
import sys


def list_palettes(palettes_path: str):
    if not os.path.isdir(palettes_path):
        print(f"Directory '{palettes_path}' not found.")
        return

    palette_files = [f for f in os.listdir(
        palettes_path) if f.endswith(".yaml")]
    palette_names = [os.path.splitext(f)[0] for f in palette_files]

    if not palette_names:
        print("No palettes found.")
    else:
        print("Available palettes:")
        for name in palette_names:
            print(f"- {name}")


def parse_palette_file(palette_file: str) -> dict:
    colors = {}

    if not os.path.isfile(palette_file):
        print(f"Palette file not found: {palette_file}")
        sys.exit(1)

    with open(palette_file, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            try:
                key, value = line.split(":", 1)
            except ValueError:
                continue

            key = key.strip()
            value = value.strip()

            m = re.match(r'^"(.*)"', value)
            if m:
                value = m.group(1).strip()
                if value.startswith("#"):
                    value = value[1:]
            else:
                continue

            colors[key] = value

    errors = []
    required_keys = {f"base{'{:02X}'.format(i)}" for i in range(16)}
    for key in required_keys:
        if key not in colors:
            errors.append(f"Missing required key: {key}")
        elif not re.match(r"^[0-9a-fA-F]{6}$", colors[key]):
            errors.append(f"Invalid color value for {key}: {colors[key]}")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    return colors


def print_palette(colors: dict):
    print("\nColor Palette Preview:")
    for key, value in colors.items():
        r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
        print(f"{key}: \033[48;2;{r};{g};{b}m  \033[0m #{value}")
