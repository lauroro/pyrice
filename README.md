# pyrice

A simple, no-dependencies tool to handle [base16](https://github.com/chriskempson/base16) powered ricing on Linux.

----------

## Overview
**pyrice** is a lightweight command-line utility for managing and applying **base16** color palettes across your Linux setup.
Since version 2.0.0, themes are applied via inline template processing. Now you can directly embed color placeholders in your configuration files using the following syntax:

```
<%pyrice:<key>:<oldvalue>>
```
Where:

-   `<key>` is a base16 key (e.g., `base00`, `base05`, etc.)
    
-   `<oldvalue>` is the current color value in the file that will be replaced.

In short:
- No external dependencies (pure Python standard library)
- Inline directive-based color substitution
- Configurable post-commands

----------

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
source venv/bin/activate
pip install -e .
```

----------

After installation, run:

```
pyrice --help
```

----------

## Configuration

Directory structure under `XDG_CONFIG_HOME/pyrice` (default: `~/.config/pyrice`):

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
  - ~/.config/alacritty/alacritty.yml
  - ~/.themes/colors.css

cmds:
  - pkill -USR1 alacritty
  - notify-send "Theme applied"
```

### Example: `palettes/nord.yaml`

```
base00: "#2E3440"
base01: "#3B4252"
...
base0F: "#B48EAD"
```

### Example: Inline Template File

File: `alacritty.yml`
```
# <%pyrice:base00:2E3440>
background: 2E3440
# <%pyrice:base08:88C0D0>
foreground: 88C0D0
```

After running `pyrice nord --rice`, the file will be updated automatically with new palette colors:

```
# <%pyrice:base00:3B4252>
background: 3B4252
# <%pyrice:base08:81A1C1>
foreground: 81A1C1
```

Multiple directives in a single line are supported:
```
# <%pyrice:base00:3B4252> <%pyrice:base08:81A1C1>
```

----------

## Usage

### Show help 
```
pyrice --help
or
pyrice -h
```

### Show version
```
pyrice --version
or
pyrice -v
```

### List available palettes
```
pyrice --list
or
pyrice -l
```

### Preview a palette in the terminal
```
pyrice --preview gruvbox
or
pyrice -p gruvbox
```

### Apply a palette
This will process inline directives and run commands
```
pyrice --rice nord
or
pyrice -r nord
```

You can also combine preview and apply:
```
pyrice --preview --rice solarized-dark
or
pyrice -pr solarized-dark
```

## 💖 Support 💖

If you like this project or find it useful, please consider making a donation to these organizations and join me in supporting them:

- 👶 [UNICEF](https://www.unicef.org/)
- 🐼 [WWF](https://www.worldwildlife.org/)

If you prefer to support me instead, you can do it:
- ☕ [Ko-fi](https://ko-fi.com/roro0)


Thank you!

----------

## License

Licensed under the GNU GPL-3.0-or-later. 

© 2025 roro
