# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from pyrice.templates import process_templates


# ---------- FIXTURES ----------
@pytest.fixture
def write(tmp_path):
    """Scrive un file all’interno di tmp_path e restituisce il path."""
    def _write(filename, content):
        p = tmp_path / filename
        p.write_text(content)
        return p
    return _write


@pytest.fixture
def read():
    """Legge un file e restituisce una lista di righe."""
    def _read(path):
        return path.read_text().splitlines()
    return _read


# ---------- TEST: process_templates ----------
def test_process_single_directive(write, read):
    f = write(
        "test.txt",
        "// <%pyrice:base00:aaaaaa>\n"
        "color = aaaaaa\n"
        "another_color = aaaaaa\n"
    )

    colors = {"base00": "111111"}

    errors = process_templates(colors, [str(f)])
    assert errors == []

    result = read(f)

    assert result[0] == "// <%pyrice:base00:111111>"
    assert result[1] == "color = 111111"
    assert result[2] == "another_color = aaaaaa"


def test_process_multiple_directives_same_line(write, read):
    f = write(
        "test.txt",
        "# <%pyrice:base00:aaaaaa>   <%pyrice:base05:ffffff>\n"
        "bg = aaaaaa; fg = ffffff\n"
    )

    colors = {"base00": "111111", "base05": "222222"}

    errors = process_templates(colors, [str(f)])
    assert errors == []

    out = read(f)
    assert out[0] == "# <%pyrice:base00:111111>   <%pyrice:base05:222222>"
    assert out[1] == "bg = 111111; fg = 222222"


def test_process_missing_key_is_ignored(write, read):
    f = write(
        "test.txt",
        "<%pyrice:base99:aaaaaa>\n"
        "color = aaaaaa\n"
    )

    colors = {"base00": "111111"}  # no base99

    process_templates(colors, [str(f)])
    out = read(f)

    assert out[0] == "<%pyrice:base99:aaaaaa>"
    assert out[1] == "color = aaaaaa"


def test_process_templates_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"
    errors = process_templates({"base00": "111111"}, [str(missing)])

    assert len(errors) == 1
    assert "Could not find file" in errors[0]


def test_process_templates_multiple_files(write, read):
    colors = {"base00": "000111"}

    paths = [
        write(f"file{i}.txt", "<%pyrice:base00:aaaaaa>\n" f"set{i} = aaaaaa\n")
        for i in range(2)
    ]

    errors = process_templates(colors, [str(p) for p in paths])
    assert errors == []

    for i, p in enumerate(paths):
        out = read(p)
        assert out[0] == "<%pyrice:base00:000111>"
        assert out[1] == f"set{i} = 000111"


def test_process_directive_without_next_line(write):
    f = write("test.txt", "<%pyrice:base00:aaaaaa>")

    colors = {"base00": "111111"}

    process_templates(colors, [str(f)])

    assert f.read_text() == "<%pyrice:base00:aaaaaa>"


def test_process_color_used_multiple_times(write, read):
    f = write(
        "multi.txt",
        "<%pyrice:base00:aaaaaa>\n"
        "color1 = #aaaaaa, color2 = #bbbbbb, color3 = #aaaaaa"
    )

    colors = {"base00": "111111"}

    errors = process_templates(colors, [str(f)])
    assert errors == []

    lines = read(f)

    assert lines[0] == "<%pyrice:base00:111111>"
    assert lines[1] == (
        "color1 = #111111, color2 = #bbbbbb, color3 = #111111"
    )
