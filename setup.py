#!/usr/bin/env python
"""
Build script for turbojpeg-torch - Python bindings for libjpeg-turbo with PyTorch support.

This module provides fast JPEG encoding/decoding using libjpeg-turbo,
with native support for PyTorch tensors.
"""

import re
import subprocess

from setuptools import setup

BASE_VERSION = "2.0.0"


def get_turbojpeg_version():
    """Detect libjpeg-turbo version and return a version suffix like 'tj212'."""
    # Try pkg-config first
    try:
        result = subprocess.run(
            ["pkg-config", "--modversion", "libturbojpeg"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            # Parse version like "2.1.2" -> "tj212"
            match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
            if match:
                major, minor, patch = match.groups()
                return f"tj{major}{minor}{patch}"
    except FileNotFoundError:
        pass

    # Try dpkg on Debian/Ubuntu
    for pkg_name in ["libturbojpeg", "libturbojpeg0", "libjpeg-turbo8"]:
        try:
            result = subprocess.run(
                ["dpkg-query", "-W", "-f=${Version}", pkg_name],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                # Parse version like "2.1.2-0ubuntu1" -> "tj212"
                match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
                if match:
                    major, minor, patch = match.groups()
                    return f"tj{major}{minor}{patch}"
        except FileNotFoundError:
            pass

    # Try rpm on RHEL/Fedora
    try:
        result = subprocess.run(
            ["rpm", "-q", "--queryformat", "%{VERSION}", "libjpeg-turbo-devel"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
            if match:
                major, minor, patch = match.groups()
                return f"tj{major}{minor}{patch}"
    except FileNotFoundError:
        pass

    # Try brew on macOS
    try:
        result = subprocess.run(
            ["brew", "list", "--versions", "jpeg-turbo"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            # Output like "jpeg-turbo 2.1.2"
            version = result.stdout.strip()
            match = re.search(r"(\d+)\.(\d+)\.(\d+)", version)
            if match:
                major, minor, patch = match.groups()
                return f"tj{major}{minor}{patch}"
    except FileNotFoundError:
        pass

    # Fallback - no version suffix
    return None


def get_version():
    """Get full version string with optional turbojpeg suffix."""
    tj_suffix = get_turbojpeg_version()
    if tj_suffix:
        return f"{BASE_VERSION}+{tj_suffix}"
    return BASE_VERSION


setup(
    version=get_version(),
    packages=["turbojpeg"],
    package_data={
        "turbojpeg_libs": ["*.so*", "*.dylib", "*.dll"],
    },
)
