"""Version management for MSH file format support.

This module provides functionality to detect, validate, and manage
different versions of the Gmsh MSH file format.
"""

from typing import Tuple, List
from enum import Enum


class MshFormatVersion(Enum):
    """Enumeration of supported MSH format versions."""

    MSH_1_0 = (1, 0)
    MSH_2_0 = (2, 0)
    MSH_2_1 = (2, 1)
    MSH_2_2 = (2, 2)
    MSH_4_0 = (4, 0)
    MSH_4_1 = (4, 1)

    def __init__(self, major: int, minor: int):
        self.major = major
        self.minor = minor

    @property
    def version_number(self) -> float:
        """Return version as float (e.g., 4.1)."""
        return float(f"{self.major}.{self.minor}")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __repr__(self) -> str:
        return f"MshFormatVersion({self.major}.{self.minor})"


class VersionManager:
    """Manager for MSH format version detection and validation."""

    # Currently supported versions
    SUPPORTED_VERSIONS = [
        MshFormatVersion.MSH_1_0,
        MshFormatVersion.MSH_2_0,
        MshFormatVersion.MSH_2_1,
        MshFormatVersion.MSH_2_2,
        MshFormatVersion.MSH_4_0,
        MshFormatVersion.MSH_4_1,
    ]

    # Versions that are recognized but not fully implemented yet
    RECOGNIZED_VERSIONS = [
        MshFormatVersion.MSH_1_0,
        MshFormatVersion.MSH_2_0,
        MshFormatVersion.MSH_2_1,
        MshFormatVersion.MSH_2_2,
        MshFormatVersion.MSH_4_0,
        MshFormatVersion.MSH_4_1,
    ]

    @staticmethod
    def parse_version(version_str: str) -> Tuple[int, int]:
        """Parse version string to major and minor version numbers.

        Parameters
        ----------
        version_str : str
            Version string (e.g., "4.1" or "2.2")

        Returns
        -------
        Tuple[int, int]
            Tuple of (major, minor) version numbers

        Raises
        ------
        ValueError
            If version string cannot be parsed
        """
        try:
            version_float = float(version_str)
            major = int(version_float)
            # Extract minor version from decimal part
            minor = int(round((version_float - major) * 10))
            return (major, minor)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid version string: {version_str}") from e

    @classmethod
    def get_version_enum(cls, major: int, minor: int) -> MshFormatVersion:
        """Get MshFormatVersion enum from major and minor version numbers.

        Parameters
        ----------
        major : int
            Major version number
        minor : int
            Minor version number

        Returns
        -------
        MshFormatVersion
            Version enum if found

        Raises
        ------
        ValueError
            If version is not recognized
        """
        for version in cls.RECOGNIZED_VERSIONS:
            if version.major == major and version.minor == minor:
                return version
        raise ValueError(f"Unrecognized MSH format version: {major}.{minor}")

    @classmethod
    def is_supported(cls, version: MshFormatVersion) -> bool:
        """Check if a version is supported.

        Parameters
        ----------
        version : MshFormatVersion
            Version to check

        Returns
        -------
        bool
            True if version is supported
        """
        return version in cls.SUPPORTED_VERSIONS

    @classmethod
    def validate_version(cls, version_str: str) -> MshFormatVersion:
        """Parse and validate a version string.

        Parameters
        ----------
        version_str : str
            Version string to validate

        Returns
        -------
        MshFormatVersion
            Validated version enum

        Raises
        ------
        ValueError
            If version is not recognized or not supported
        """
        major, minor = cls.parse_version(version_str)
        version_enum = cls.get_version_enum(major, minor)

        if not cls.is_supported(version_enum):
            supported = ", ".join(str(v) for v in cls.SUPPORTED_VERSIONS)
            raise ValueError(
                f"MSH format version {major}.{minor} is recognized but not "
                f"supported. Supported versions: {supported}"
            )

        return version_enum

    @classmethod
    def is_version_1(cls, version: MshFormatVersion) -> bool:
        """Check if version is in the 1.x series.

        Parameters
        ----------
        version : MshFormatVersion
            Version to check

        Returns
        -------
        bool
            True if version is 1.x
        """
        return version.major == 1

    @classmethod
    def is_version_2(cls, version: MshFormatVersion) -> bool:
        """Check if version is in the 2.x series.

        Parameters
        ----------
        version : MshFormatVersion
            Version to check

        Returns
        -------
        bool
            True if version is 2.x
        """
        return version.major == 2

    @classmethod
    def is_version_4(cls, version: MshFormatVersion) -> bool:
        """Check if version is in the 4.x series.

        Parameters
        ----------
        version : MshFormatVersion
            Version to check

        Returns
        -------
        bool
            True if version is 4.x
        """
        return version.major == 4

    @classmethod
    def get_supported_versions_list(cls) -> List[str]:
        """Get list of supported version strings.

        Returns
        -------
        List[str]
            List of supported version strings
        """
        return [str(v) for v in cls.SUPPORTED_VERSIONS]
