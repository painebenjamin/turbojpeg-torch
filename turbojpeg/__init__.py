"""
turbojpeg-torch: Fast JPEG encoding/decoding with libjpeg-turbo and PyTorch support.

This module provides hardware-accelerated JPEG operations using libjpeg-turbo,
with native support for PyTorch tensors.
"""

# Import torch first to ensure its libraries are loaded before we use them
import torch  # noqa: F401

from turbojpeg.turbojpeg import (
    TurboJPEG,
    # Color spaces
    TJCS_RGB,
    TJCS_YCbCr,
    TJCS_GRAY,
    TJCS_CMYK,
    TJCS_YCCK,
    # Pixel formats
    TJPF_RGB,
    TJPF_BGR,
    TJPF_RGBX,
    TJPF_BGRX,
    TJPF_XBGR,
    TJPF_XRGB,
    TJPF_GRAY,
    TJPF_RGBA,
    TJPF_BGRA,
    TJPF_ABGR,
    TJPF_ARGB,
    TJPF_CMYK,
    # Chrominance subsampling options
    TJSAMP_444,
    TJSAMP_422,
    TJSAMP_420,
    TJSAMP_GRAY,
    TJSAMP_440,
    TJSAMP_411,
    TJSAMP_441,
    # Transform operations
    TJXOP_NONE,
    TJXOP_HFLIP,
    TJXOP_VFLIP,
    TJXOP_TRANSPOSE,
    TJXOP_TRANSVERSE,
    TJXOP_ROT90,
    TJXOP_ROT180,
    TJXOP_ROT270,
    # Transform options
    TJXOPT_PERFECT,
    TJXOPT_TRIM,
    TJXOPT_CROP,
    TJXOPT_GRAY,
    TJXOPT_NOOUTPUT,
    TJXOPT_PROGRESSIVE,
    TJXOPT_COPYNONE,
    # Flags
    TJFLAG_BOTTOMUP,
    TJFLAG_FASTUPSAMPLE,
    TJFLAG_FASTDCT,
    TJFLAG_ACCURATEDCT,
    TJFLAG_STOPONWARNING,
    TJFLAG_PROGRESSIVE,
    TJFLAG_LIMITSCANS,
)

__version__ = "1.8.2"

__all__ = [
    "TurboJPEG",
    # Color spaces
    "TJCS_RGB",
    "TJCS_YCbCr",
    "TJCS_GRAY",
    "TJCS_CMYK",
    "TJCS_YCCK",
    # Pixel formats
    "TJPF_RGB",
    "TJPF_BGR",
    "TJPF_RGBX",
    "TJPF_BGRX",
    "TJPF_XBGR",
    "TJPF_XRGB",
    "TJPF_GRAY",
    "TJPF_RGBA",
    "TJPF_BGRA",
    "TJPF_ABGR",
    "TJPF_ARGB",
    "TJPF_CMYK",
    # Chrominance subsampling options
    "TJSAMP_444",
    "TJSAMP_422",
    "TJSAMP_420",
    "TJSAMP_GRAY",
    "TJSAMP_440",
    "TJSAMP_411",
    "TJSAMP_441",
    # Transform operations
    "TJXOP_NONE",
    "TJXOP_HFLIP",
    "TJXOP_VFLIP",
    "TJXOP_TRANSPOSE",
    "TJXOP_TRANSVERSE",
    "TJXOP_ROT90",
    "TJXOP_ROT180",
    "TJXOP_ROT270",
    # Transform options
    "TJXOPT_PERFECT",
    "TJXOPT_TRIM",
    "TJXOPT_CROP",
    "TJXOPT_GRAY",
    "TJXOPT_NOOUTPUT",
    "TJXOPT_PROGRESSIVE",
    "TJXOPT_COPYNONE",
    # Flags
    "TJFLAG_BOTTOMUP",
    "TJFLAG_FASTUPSAMPLE",
    "TJFLAG_FASTDCT",
    "TJFLAG_ACCURATEDCT",
    "TJFLAG_STOPONWARNING",
    "TJFLAG_PROGRESSIVE",
    "TJFLAG_LIMITSCANS",
]

