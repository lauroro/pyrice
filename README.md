# pyrice

A simple, no-dependencies tool to handle [base16](https://github.com/chriskempson/base16) powered ricing on Linux.

---

## Overview

**pyrice** is a lightweight command-line utility for managing and applying **base16** color palettes across your Linux setup.
It replaces color placeholders like ``{{base00}}`` in template files and can execute post-processing commands after applying a theme.

- No external dependencies (pure Python standard library)
- Template-based color substitution
- Configurable post-commands

---

## Installation

### Using pipx (recommended)

```
git clone https://codeberg.org/roro/pyrice
cd pyrice
pipx install -e .
```

### Local installation

```
git clone https://codeberg.org/roro/pyrice
cd pyrice
python -m venv venv
source venv/bin/activate # or source venv/bin/activate.fish
pip install -e .
```

---

After installation, run:

```
pyrice --help
```

---

## Configuration

pyrice expects a directory structure under `XDG_CONFIG_HOME/pyrice`, assuming  `~/.config/pyrice` as fallback/default:

```
~/.config/pyrice/
├── config.yaml
└── palettes/
    ├── nord.yaml
    ├── gruvbox.yaml
    └── dracula.yaml
```

### Example: `config.yaml`

```
paths:
  - ~/.config/alacritty/template.yml
  - ~/.themes/template.css

cmds:
  - pkill -USR1 alacritty
  - notify-send "Theme applied"
```

### Example: `palettes/nord.yaml`

```
base00: "#2E3440"
base01: "#3B4252"
base02: "#434C5E"
base03: "#4C566A"
base04: "#D8DEE9"
base05: "#E5E9F0"
base06: "#ECEFF4"
base07: "#8FBCBB"
base08: "#88C0D0"
base09: "#81A1C1"
base0A: "#5E81AC"
base0B: "#BF616A"
base0C: "#D08770"
base0D: "#EBCB8B"
base0E: "#A3BE8C"
base0F: "#B48EAD"
```

### Example: Template file 

Let's assume we have a file `template.colors.yml` properly addressed in the config file:

```
colors:
  primary: "{{base00}}"
  accent: "{{base08}}"
```
pyrice will produce a new file `colors.yml`:
```
colors:
  primary: "2E3440"
  accent: "88C0D0"
```

---

## Usage

List available palettes:
```
pyrice --list
```
or
```
pyrice -l
```
---
Preview a palette in the terminal:
```
pyrice nord --preview
```
or
```
pyrice nord -p
```
---
Apply a palette (process templates and run commands):
```
pyrice nord --rice
```
or
```
pyrice nord -r
```
---
Tip: you can also combine `-p` and `-r` (or `-pr`) to both print the palette preview and apply it.

---

## License

Licensed under the GNU GPL-3.0-or-later.
© 2025 roro
