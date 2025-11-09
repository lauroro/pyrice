# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from pyrice import config


# ---------- FIXTURES ----------
@pytest.fixture
def config_file_valid(tmp_path):
    file = tmp_path / "config.yaml"
    file.write_text("""
paths:
  - ~/.config/template.file
  - ~/.themes/template.other
cmds:
  - reload-theme
  - notify-send 'done'
""")
    return file


@pytest.fixture
def config_file_empty(tmp_path):
    file = tmp_path / "empty.yaml"
    file.write_text("# empty config")
    return file


# ---------- TEST: parse_config_file ----------
def test_parse_config_file_valid(config_file_valid):
    paths, cmds = config.parse_config_file(str(config_file_valid))
    assert len(paths) == 2
    assert "~/.config/template.file" in paths
    assert "reload-theme" in cmds


def test_parse_config_file_missing_sections(config_file_empty, capsys):
    with pytest.raises(SystemExit):
        config.parse_config_file(str(config_file_empty))
    out = capsys.readouterr().out
    assert "No valid sections" in out


def test_parse_config_file_not_found(capsys):
    with pytest.raises(SystemExit):
        config.parse_config_file("/nonexistent/config.yaml")
    out = capsys.readouterr().out
    assert "not found" in out
