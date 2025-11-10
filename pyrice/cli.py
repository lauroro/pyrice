# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import argparse

from pyrice.palettes import list_palettes, parse_palette_file, print_palette
from pyrice.config import parse_config_file
from pyrice.templates import process_templates
from pyrice.commands import execute_commands


def main():
    parser = argparse.ArgumentParser(
        description="pyrice, a tool to handle your base16 powered rice")
    parser.add_argument("palette_name", nargs="?",
                        help="palette name, file name without extension")
    parser.add_argument("-l", "--list", action="store_true",
                        help="List defined palettes")
    parser.add_argument("-p", "--preview", action="store_true",
                        help="Preview the palette")
    parser.add_argument("-r", "--rice", action="store_true",
                        help="Perform the ricing")
    args = parser.parse_args()

    config_home = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    pyrice_dir = os.path.join(config_home, "pyrice")
    palette_file = os.path.join(
        pyrice_dir, f"palettes/{args.palette_name}.yaml")
    config_file = os.path.join(pyrice_dir, "config.yaml")

    if args.list:
        list_palettes(os.path.join(pyrice_dir, "palettes"))
        sys.exit(0)

    if not args.list and len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)

    if not os.path.isfile(config_file) or not os.path.isfile(palette_file):
        print("Config or palette file not found.")
        sys.exit(1)

    colors = parse_palette_file(palette_file)

    if args.preview:
        print_palette(colors)

    if not args.rice:
        sys.exit(0)

    paths, cmds = parse_config_file(config_file)
    errors = process_templates(colors, paths) + execute_commands(cmds)
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
