"""Tests for version_manager module."""

import pytest
from gmshparser.version_manager import (
    VersionManager,
    MshFormatVersion,
)


def test_parse_version():
    """Test parsing version strings."""
    assert VersionManager.parse_version("4.1") == (4, 1)
    assert VersionManager.parse_version("2.2") == (2, 2)
    assert VersionManager.parse_version("4.0") == (4, 0)

    with pytest.raises(ValueError):
        VersionManager.parse_version("invalid")

    with pytest.raises(ValueError):
        VersionManager.parse_version("abc")


def test_get_version_enum():
    """Test getting version enum from major/minor."""
    version = VersionManager.get_version_enum(4, 1)
    assert version == MshFormatVersion.MSH_4_1
    assert version.major == 4
    assert version.minor == 1
    assert version.version_number == 4.1

    version = VersionManager.get_version_enum(2, 2)
    assert version == MshFormatVersion.MSH_2_2

    with pytest.raises(ValueError):
        VersionManager.get_version_enum(99, 99)


def test_is_supported():
    """Test checking if version is supported."""
    assert VersionManager.is_supported(MshFormatVersion.MSH_4_1)
    assert VersionManager.is_supported(MshFormatVersion.MSH_4_0)
    assert VersionManager.is_supported(MshFormatVersion.MSH_2_2)
    # MSH 1.0, 2.0, and 2.1 are now supported
    assert VersionManager.is_supported(MshFormatVersion.MSH_2_1)
    assert VersionManager.is_supported(MshFormatVersion.MSH_2_0)
    assert VersionManager.is_supported(MshFormatVersion.MSH_1_0)


def test_validate_version():
    """Test full version validation."""
    # Valid supported versions
    version = VersionManager.validate_version("4.1")
    assert version == MshFormatVersion.MSH_4_1

    version = VersionManager.validate_version("2.2")
    assert version == MshFormatVersion.MSH_2_2

    version = VersionManager.validate_version("2.0")
    assert version == MshFormatVersion.MSH_2_0

    version = VersionManager.validate_version("1.0")
    assert version == MshFormatVersion.MSH_1_0

    # Unrecognized version (use 3.0 which doesn't exist)
    with pytest.raises(ValueError, match="Unrecognized"):
        VersionManager.validate_version("99.9")


def test_is_version_2():
    """Test checking for version 2.x."""
    assert VersionManager.is_version_2(MshFormatVersion.MSH_2_2)
    assert VersionManager.is_version_2(MshFormatVersion.MSH_2_1)
    assert VersionManager.is_version_2(MshFormatVersion.MSH_2_0)
    assert not VersionManager.is_version_2(MshFormatVersion.MSH_4_1)
    assert not VersionManager.is_version_2(MshFormatVersion.MSH_4_0)
    assert not VersionManager.is_version_2(MshFormatVersion.MSH_1_0)


def test_is_version_4():
    """Test checking for version 4.x."""
    assert VersionManager.is_version_4(MshFormatVersion.MSH_4_1)
    assert VersionManager.is_version_4(MshFormatVersion.MSH_4_0)
    assert not VersionManager.is_version_4(MshFormatVersion.MSH_2_2)
    assert not VersionManager.is_version_4(MshFormatVersion.MSH_2_1)
    assert not VersionManager.is_version_4(MshFormatVersion.MSH_1_0)


def test_is_version_1():
    """Test checking for version 1.x."""
    assert VersionManager.is_version_1(MshFormatVersion.MSH_1_0)
    assert not VersionManager.is_version_1(MshFormatVersion.MSH_2_2)
    assert not VersionManager.is_version_1(MshFormatVersion.MSH_4_1)


def test_get_supported_versions_list():
    """Test getting list of supported versions."""
    versions = VersionManager.get_supported_versions_list()
    assert isinstance(versions, list)
    assert "4.1" in versions
    assert "4.0" in versions
    assert "2.2" in versions
    assert "2.1" in versions
    assert "2.0" in versions
    assert "1.0" in versions


def test_version_enum_properties():
    """Test MshFormatVersion enum properties."""
    v41 = MshFormatVersion.MSH_4_1
    assert v41.major == 4
    assert v41.minor == 1
    assert v41.version_number == 4.1
    assert str(v41) == "4.1"
    assert "4.1" in repr(v41)
