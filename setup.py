#!/usr/bin/env python
"""
Build script for turbojpeg-torch - Python bindings for libjpeg-turbo with PyTorch support.

This module provides fast JPEG encoding/decoding using libjpeg-turbo,
with native support for PyTorch tensors.
"""

import re

from setuptools import setup

# Base version - torch suffix will be appended
BASE_VERSION = "1.8.2"


def get_torch_version():
    """Get PyTorch version string like 'torch2.5'."""
    try:
        import torch
        version = torch.__version__
        # Parse version like "2.5.0+cu124" or "2.5.0"
        match = re.match(r"(\d+)\.(\d+)", version)
        if match:
            major, minor = match.groups()
            return f"torch{major}.{minor}"
    except ImportError:
        pass
    return "torch2.0"  # Default fallback


def get_version():
    """Get full version string with torch suffix."""
    torch_suffix = get_torch_version()
    return f"{BASE_VERSION}+{torch_suffix}"


setup(
    version=get_version(),
    packages=["turbojpeg"],
    package_data={
        "turbojpeg_libs": ["*.so*", "*.dylib", "*.dll"],
    },
)
