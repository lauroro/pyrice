# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from pyrice import config


# ---------- TEST: parse_config_file ----------
def test_parse_config_file_valid(tmp_path):
    file = tmp_path / "config.yaml"
    file.write_text("""
paths:
  - ~/.config/template.file
  - ~/.themes/template.other
cmds:
  - reload-theme
  - notify-send 'done'
""")
    paths, cmds = config.parse_config_file(str(file))
    assert len(paths) == 2
    assert "~/.config/template.file" in paths
    assert "reload-theme" in cmds


def test_parse_config_file_missing_sections(tmp_path, capsys):
    file = tmp_path / "config.yaml"
    file.write_text("# no sections here\n")
    with pytest.raises(SystemExit):
        config.parse_config_file(str(file))
    out = capsys.readouterr().out
    assert "No valid sections" in out


def test_parse_config_file_not_found(capsys):
    with pytest.raises(SystemExit):
        config.parse_config_file("/nonexistent/config.yaml")
    out = capsys.readouterr().out
    assert "not found" in out
