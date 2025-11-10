# SPDX-FileCopyrightText: 2025 roro
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import pytest
from pyrice import cli


# ---------- FIXTURES ----------
@pytest.fixture(autouse=True)
def no_sys_exit(monkeypatch):
    # this prevents sys.exit from closing pytest by raising SystemExit instead
    def fake_exit(code=0):
        raise SystemExit(code)
    monkeypatch.setattr(sys, "exit", fake_exit)


@pytest.fixture
def fake_paths(tmp_path, monkeypatch):
    cfg = tmp_path / "pyrice"
    pal_dir = cfg / "palettes"
    pal_dir.mkdir(parents=True)
    palette = pal_dir / "test.yaml"
    palette.write_text(
        "base00: #000000\n" +
        "\n".join([f"base{num:02X}: #111111" for num in range(1, 16)])
    )
    config = cfg / "config.yaml"
    config.write_text("paths: []\ncmds: []\n")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    return palette, config


# ---------- TEST: cli ----------
def test_cli_list(monkeypatch, capsys, fake_paths):
    called = {}

    def fake_list(path):
        called["ok"] = True
        print("Available palettes:")

    monkeypatch.setattr(cli, "list_palettes", fake_list)
    monkeypatch.setattr(sys, "argv", ["prog", "--list"])

    with pytest.raises(SystemExit) as e:
        cli.main()

    out = capsys.readouterr().out
    assert "Available palettes:" in out
    assert called.get("ok")
    assert e.value.code == 0


def test_cli_missing_args(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog"])
    with pytest.raises(SystemExit) as e:
        cli.main()
    out = capsys.readouterr().out
    assert "usage:" in out
    assert e.value.code == 1


def test_cli_missing_files(monkeypatch, capsys, tmp_path):
    # set XDG_CONFIG_HOME to an empty tmp dir so config/palette are missing
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["prog", "nonexistent", "--rice"])
    with pytest.raises(SystemExit) as e:
        cli.main()
    out = capsys.readouterr().out
    assert "Config or palette file not found" in out
    assert e.value.code == 1


def test_cli_preview(monkeypatch, fake_paths):
    monkeypatch.setattr(cli, "parse_palette_file",
                        lambda _: {"base00": "000000"})
    called = {}
    monkeypatch.setattr(cli, "print_palette",
                        lambda _: called.setdefault("preview", True))
    monkeypatch.setattr(sys, "argv", ["prog", "test", "--preview"])

    with pytest.raises(SystemExit) as e:
        cli.main()

    assert called.get("preview")
    assert e.value.code == 0


def test_cli_rice(monkeypatch, fake_paths):
    monkeypatch.setattr(cli, "parse_palette_file",
                        lambda _: {"base00": "000000"})
    monkeypatch.setattr(cli, "parse_config_file", lambda _: (["a"], ["b"]))
    monkeypatch.setattr(cli, "process_templates", lambda _, __: [])
    monkeypatch.setattr(cli, "execute_commands", lambda _: [])
    monkeypatch.setattr(sys, "argv", ["prog", "test", "--rice"])

    with pytest.raises(SystemExit) as e:
        cli.main()

    assert e.value.code == 0


def test_cli_rice_with_errors(monkeypatch, fake_paths, capsys):
    monkeypatch.setattr(cli, "parse_palette_file",
                        lambda _: {"base00": "000000"})
    monkeypatch.setattr(cli, "parse_config_file", lambda _: (["a"], ["b"]))
    monkeypatch.setattr(cli, "process_templates", lambda c, p: ["error 1"])
    monkeypatch.setattr(cli, "execute_commands", lambda c: ["error 2"])
    monkeypatch.setattr(sys, "argv", ["prog", "test", "--rice"])

    with pytest.raises(SystemExit) as e:
        cli.main()

    out = capsys.readouterr().out
    assert "error 1" in out
    assert "error 2" in out
    assert e.value.code == 1
