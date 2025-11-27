#!/usr/bin/env python
"""
Bundle libjpeg-turbo libraries into the wheel.

This script copies the required libjpeg-turbo shared libraries into the wheel
so the package is self-contained and doesn't require system-level installation.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile


def get_turbojpeg_lib_path():
    """Find libjpeg-turbo library path."""
    system = platform.system()
    
    if system == "Linux":
        # Common Linux paths for libjpeg-turbo
        common_paths = [
            "/usr/lib/x86_64-linux-gnu",
            "/usr/lib64",
            "/usr/lib",
            "/opt/libjpeg-turbo/lib64",
            "/usr/local/lib",
        ]
        lib_name = "libturbojpeg.so.0"
    elif system == "Darwin":
        # macOS paths
        common_paths = [
            "/usr/local/opt/jpeg-turbo/lib",
            "/opt/homebrew/opt/jpeg-turbo/lib",
            "/opt/libjpeg-turbo/lib64",
        ]
        lib_name = "libturbojpeg.dylib"
    elif system == "Windows":
        common_paths = [
            "C:/libjpeg-turbo64/bin",
            "C:/libjpeg-turbo/bin",
        ]
        lib_name = "turbojpeg.dll"
    else:
        return None, None

    for path in common_paths:
        lib_path = os.path.join(path, lib_name)
        if os.path.exists(lib_path):
            return path, lib_name

    return None, None


def find_library(lib_name: str, search_paths: list) -> Path | None:
    """Find a library file in the search paths."""
    for search_path in search_paths:
        path = Path(search_path)
        if not path.exists():
            continue
        # Look for the library (handle symlinks)
        for lib_file in path.glob(f"{lib_name}*"):
            if lib_file.is_file():
                # Follow symlink to get the real file
                real_path = lib_file.resolve()
                if real_path.exists():
                    return real_path
    return None


def patch_rpath(lib_path: Path, new_rpath: str):
    """Patch the RPATH of a library using patchelf (Linux only)."""
    if platform.system() != "Linux":
        return
    try:
        subprocess.run(
            ["patchelf", "--set-rpath", new_rpath, str(lib_path)],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to patch RPATH for {lib_path}: {e}")
    except FileNotFoundError:
        print("Warning: patchelf not found. RPATH not patched.")


def bundle_wheel(wheel_path: str, output_dir: str = None) -> str:
    """
    Bundle libjpeg-turbo libraries into a wheel.

    Args:
        wheel_path: Path to the input wheel file
        output_dir: Output directory for the bundled wheel

    Returns:
        Path to the bundled wheel
    """
    wheel_path = Path(wheel_path)
    if output_dir is None:
        output_dir = wheel_path.parent
    output_dir = Path(output_dir)

    lib_dir, lib_name = get_turbojpeg_lib_path()
    if not lib_dir:
        raise RuntimeError(
            "Could not find libjpeg-turbo library. "
            "Please install libjpeg-turbo:\n"
            "  Linux: sudo apt-get install libturbojpeg\n"
            "  macOS: brew install jpeg-turbo\n"
            "  Windows: Download from https://libjpeg-turbo.org/"
        )

    print(f"Using libjpeg-turbo from: {lib_dir}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        extract_dir = tmpdir / "wheel"

        # Extract wheel
        print(f"Extracting wheel: {wheel_path}")
        with ZipFile(wheel_path, "r") as zf:
            zf.extractall(extract_dir)

        # Create libs directory
        libs_dir = extract_dir / "turbojpeg_libs"
        libs_dir.mkdir(exist_ok=True)

        # Copy the main library
        system = platform.system()
        lib_path = Path(lib_dir) / lib_name
        
        if lib_path.is_symlink():
            # Get the real file
            real_lib = lib_path.resolve()
            dest = libs_dir / real_lib.name
            print(f"Bundling: {real_lib} -> {dest.name}")
            shutil.copy2(real_lib, dest)
            
            # Create symlink with the expected name
            symlink_dest = libs_dir / lib_name
            if not symlink_dest.exists():
                symlink_dest.symlink_to(dest.name)
                print(f"Created symlink: {lib_name} -> {dest.name}")
        else:
            dest = libs_dir / lib_name
            print(f"Bundling: {lib_path} -> {dest.name}")
            shutil.copy2(lib_path, dest)

        # On Linux, also copy any versioned symlinks
        if system == "Linux":
            for lib_file in Path(lib_dir).glob("libturbojpeg.so*"):
                if lib_file.is_symlink():
                    continue
                dest = libs_dir / lib_file.name
                if not dest.exists():
                    print(f"Bundling: {lib_file} -> {dest.name}")
                    shutil.copy2(lib_file, dest)

        # Patch RPATH for bundled libraries on Linux
        if system == "Linux":
            for lib_file in libs_dir.glob("*.so*"):
                if not lib_file.is_symlink():
                    patch_rpath(lib_file, "$ORIGIN")

        # Update RECORD file
        record_files = list(extract_dir.glob("*.dist-info/RECORD"))
        if record_files:
            record_file = record_files[0]
            with open(record_file, "a") as f:
                for lib_file in libs_dir.iterdir():
                    rel_path = lib_file.relative_to(extract_dir)
                    f.write(f"{rel_path},,\n")

        # Repack wheel
        output_wheel = output_dir / wheel_path.name

        print(f"Creating bundled wheel: {output_wheel}")
        with ZipFile(output_wheel, "w") as zf:
            for file_path in extract_dir.rglob("*"):
                if file_path.is_file() or file_path.is_symlink():
                    arcname = file_path.relative_to(extract_dir)
                    zf.write(file_path, arcname)

        return str(output_wheel)


def main():
    parser = argparse.ArgumentParser(
        description="Bundle libjpeg-turbo libraries into a wheel"
    )
    parser.add_argument(
        "wheel",
        help="Path to the wheel file to bundle",
    )
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory for the bundled wheel",
    )
    args = parser.parse_args()

    try:
        output = bundle_wheel(args.wheel, args.output_dir)
        print(f"\nBundled wheel created: {output}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

