# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pyrice import templates


# ---------- TEST: process_templats ----------
def test_process_templates_success(tmp_path):
    template_file = tmp_path / "template.colors"
    template_content = "background={{base00}}\nforeground={{base05}}\n"
    template_file.write_text(template_content)

    colors = {"base00": "111111", "base05": "ffffff"}

    errors = templates.process_templates(colors, [str(template_file)])
    output_file = tmp_path / "colors"

    assert errors == []
    assert output_file.exists()
    output = output_file.read_text()
    assert "111111" in output
    assert "ffffff" in output
    assert "{{base00}}" not in output


def test_process_templates_missing_file(tmp_path):
    missing_path = tmp_path / "nonexistent.yaml"
    errors = templates.process_templates({}, [str(missing_path)])
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


def test_process_templates_multiple_files(tmp_path):
    paths = []
    for i in range(2):
        f = tmp_path / f"template.{i}.txt"
        f.write_text("color={{base00}}")
        paths.append(str(f))

    colors = {"base00": "123456"}
    errors = templates.process_templates(colors, paths)

    assert errors == []
    for i in range(2):
        out_file = tmp_path / f"{i}.txt"
        assert out_file.exists()
        assert out_file.read_text() == "color=123456"
