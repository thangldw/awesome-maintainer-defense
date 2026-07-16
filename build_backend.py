"""PEP 517 backend that generates the embedded CLI module before packaging."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from setuptools import build_meta as _setuptools

ROOT = Path(__file__).resolve().parent


def _prepare() -> None:
    module = ROOT / "generated/maintainer_defense_kit.py"
    builder = ROOT / "scripts/build_standalone.py"
    if builder.is_file():
        subprocess.run([sys.executable, str(builder)], cwd=ROOT, check=True)
    elif not module.is_file():
        raise RuntimeError("source distribution is missing the generated CLI module")


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _prepare()
    return _setuptools.build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    _prepare()
    return _setuptools.build_sdist(sdist_directory, config_settings)


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    _prepare()
    return _setuptools.prepare_metadata_for_build_wheel(metadata_directory, config_settings)


def get_requires_for_build_wheel(config_settings=None):
    _prepare()
    return _setuptools.get_requires_for_build_wheel(config_settings)


def get_requires_for_build_sdist(config_settings=None):
    _prepare()
    return _setuptools.get_requires_for_build_sdist(config_settings)


if hasattr(_setuptools, "build_editable"):
    def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
        _prepare()
        return _setuptools.build_editable(
            wheel_directory, config_settings, metadata_directory
        )


    def get_requires_for_build_editable(config_settings=None):
        _prepare()
        return _setuptools.get_requires_for_build_editable(config_settings)


    def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
        _prepare()
        return _setuptools.prepare_metadata_for_build_editable(
            metadata_directory, config_settings
        )
