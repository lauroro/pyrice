# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re
import pytest
from pyrice import palettes


# ---------- FIXTURES ----------
@pytest.fixture
def palette_dir(tmp_path):
    """Create a temp directory for palettes and tests"""
    d = tmp_path / "palettes"
    d.mkdir()
    return d


@pytest.fixture
def valid_palette_file(tmp_path):
    """Create a valid palette file with every 'baseXY'"""
    file = tmp_path / "valid.yaml"
    content = "\n".join([f'base{num:02X}: "#ABCDEF"' for num in range(16)])
    file.write_text(content)
    return file


# ---------- TEST: list_palettes ----------
def test_list_palettes_found(palette_dir, capsys):
    (palette_dir / "gruvbox.yaml").write_text('base00: "#000000"')
    (palette_dir / "nord.yaml").write_text('base00: "#111111"')

    palettes.list_palettes(str(palette_dir))
    captured = capsys.readouterr()

    assert "Available palettes:" in captured.out
    assert "- gruvbox" in captured.out
    assert "- nord" in captured.out


def test_list_palettes_empty_dir(palette_dir, capsys):
    palettes.list_palettes(str(palette_dir))
    captured = capsys.readouterr()
    assert "No palettes found." in captured.out


def test_list_palettes_no_dir(capsys):
    palettes.list_palettes("/non/existent/path")
    captured = capsys.readouterr()
    assert "not found" in captured.out


# ---------- TEST: parse_palette_file ----------
def test_parse_palette_file_valid(valid_palette_file):
    colors = palettes.parse_palette_file(str(valid_palette_file))
    assert len(colors) == 16
    assert colors["base00"] == "ABCDEF"
    assert all(re.match(r"^[A-F0-9]{6}$", v) for v in colors.values())


def test_parse_palette_file_missing_key(tmp_path, capsys):
    file = tmp_path / "missing.yaml"
    file.write_text('base00: "#FFFFFF"\nbase01: "#000000"\n')
    with pytest.raises(SystemExit):
        palettes.parse_palette_file(str(file))
    captured = capsys.readouterr()
    assert "Missing required key" in captured.out


def test_parse_palette_file_invalid_value(tmp_path, capsys):
    content = "\n".join(
        [f'base{num:02X}: "#ABCDEF"' if num !=
            0 else 'base00: "#GGHHHH"' for num in range(16)]
    )
    file = tmp_path / "invalid.yaml"
    file.write_text(content)
    with pytest.raises(SystemExit):
        palettes.parse_palette_file(str(file))
    captured = capsys.readouterr()
    assert "Invalid color value" in captured.out


def test_parse_palette_file_with_inline_comments(tmp_path):
    file = tmp_path / "inline.yaml"
    content = "\n".join([
        f'base{num:02X}: "#ABCDEF"' for num in range(16)
    ])
    file.write_text(content)
    colors = palettes.parse_palette_file(str(file))
    assert len(colors) == 16
    assert colors["base00"] == "ABCDEF"


# ---------- TEST: print_palette ----------
def test_print_palette_output(capsys):
    colors = {"base00": "FF0000", "base01": "00FF00"}
    palettes.print_palette(colors)
    captured = capsys.readouterr()
    assert "Color Palette Preview" in captured.out
    assert "base00" in captured.out
    assert "#FF0000" in captured.out
