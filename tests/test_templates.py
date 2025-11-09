# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from pyrice import templates


# ---------- FIXTURES ----------
@pytest.fixture
def template_base(tmp_path):
    file = tmp_path / "template.colors"
    file.write_text("background={{base00}}\nforeground={{base05}}\n")
    colors = {"base00": "111111", "base05": "ffffff"}
    return file, colors


@pytest.fixture
def empty_colors():
    return {}


# ---------- TEST: process_templates ----------
def test_process_templates_success(template_base):
    template_file, colors = template_base

    errors = templates.process_templates(colors, [str(template_file)])
    output_file = template_file.parent / "colors"

    assert errors == []
    assert output_file.exists()
    output = output_file.read_text()
    assert "111111" in output
    assert "ffffff" in output
    assert "{{base00}}" not in output


def test_process_templates_missing_file(tmp_path, empty_colors):
    missing_path = tmp_path / "nonexistent.yaml"
    errors = templates.process_templates(empty_colors, [str(missing_path)])
    assert len(errors) == 1
    assert "Could not find file" in errors[0]


def test_process_templates_partial_replacement(tmp_path):
    template_file = tmp_path / "template.conf"
    template_file.write_text("color1={{base00}}\ncolor2={{base01}}\n")
    colors = {"base00": "AAA000"}  # no base01

    errors = templates.process_templates(colors, [str(template_file)])
    assert errors == []

    output_file = tmp_path / "conf"
    assert output_file.exists()
    content = output_file.read_text()
    assert "AAA000" in content
    assert "{{base01}}" in content  # unchanged


def test_process_templates_multiple_files(tmp_path, template_base):
    _, colors = template_base
    paths = []
    for i in range(2):
        f = tmp_path / f"template.{i}.txt"
        f.write_text("color={{base00}}")
        paths.append(str(f))

    errors = templates.process_templates(colors, paths)

    assert errors == []
    for i in range(2):
        out_file = tmp_path / f"{i}.txt"
        assert out_file.exists()
        assert out_file.read_text() == "color=111111"
