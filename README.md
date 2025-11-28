# turbojpeg-torch

A Python wrapper of libjpeg-turbo for decoding and encoding JPEG images with native PyTorch tensor support.

## Features

- **Fast JPEG encoding/decoding** using libjpeg-turbo's optimized SIMD instructions
- **Native PyTorch tensor support** - decode directly to tensors, encode from tensors
- **Bundled libraries** - no system-level libjpeg-turbo installation required (for bundled wheels)
- **Zero-copy when possible** - efficient memory handling between numpy and torch

## Installation

### From wheel (recommended)

```bash
pip install turbojpeg-torch
```

### From source

Requires libjpeg-turbo to be installed:

```bash
# macOS
brew install jpeg-turbo

# Ubuntu/Debian
sudo apt-get install libturbojpeg

# RHEL/CentOS/Fedora
sudo yum install libjpeg-turbo-official

# Then install the package
pip install .
```

## Quick Start

```python
import torch
from turbojpeg import TurboJPEG, TJPF_RGB, TJPF_BGR

# Initialize decoder/encoder
jpeg = TurboJPEG()

# Decode JPEG to PyTorch tensor (default: returns tensor)
with open('input.jpg', 'rb') as f:
    tensor = jpeg.decode(f.read())
    # tensor is a torch.Tensor with shape (H, W, 3) and dtype uint8

print(f"Shape: {tensor.shape}, dtype: {tensor.dtype}")
# Shape: torch.Size([480, 640, 3]), dtype: torch.uint8

# Decode to numpy array instead
with open('input.jpg', 'rb') as f:
    array = jpeg.decode(f.read(), as_tensor=False)
    # array is a numpy.ndarray

# Encode PyTorch tensor to JPEG
tensor = torch.zeros((480, 640, 3), dtype=torch.uint8)
tensor[:, :, 0] = 255  # Red image

jpeg_bytes = jpeg.encode(tensor, pixel_format=TJPF_RGB, quality=90)
with open('output.jpg', 'wb') as f:
    f.write(jpeg_bytes)
```

## API Reference

### TurboJPEG

```python
class TurboJPEG(lib_path=None)
```

Main class for JPEG encoding/decoding.

**Parameters:**
- `lib_path` (str, optional): Path to libjpeg-turbo library. If None, uses bundled or system library.

### decode

```python
def decode(jpeg_buf, pixel_format=TJPF_BGR, scaling_factor=None, flags=0, dst=None, as_tensor=True)
```

Decode JPEG bytes to tensor or array.

**Parameters:**
- `jpeg_buf` (bytes): JPEG image data
- `pixel_format` (int): Output pixel format (TJPF_BGR, TJPF_RGB, etc.)
- `scaling_factor` (tuple, optional): Scale factor as (num, denom)
- `flags` (int): Decoding flags
- `dst` (Tensor/ndarray, optional): Pre-allocated destination buffer
- `as_tensor` (bool): If True, return PyTorch tensor; if False, return numpy array

**Returns:**
- `torch.Tensor` or `numpy.ndarray`: Decoded image with shape (H, W, C)

### encode

```python
def encode(img_array, quality=85, pixel_format=TJPF_BGR, jpeg_subsample=TJSAMP_422, flags=0, dst=None)
```

Encode tensor or array to JPEG bytes.

**Parameters:**
- `img_array` (Tensor/ndarray): Input image with shape (H, W, C) and dtype uint8
- `quality` (int): JPEG quality (1-100)
- `pixel_format` (int): Input pixel format
- `jpeg_subsample` (int): Chrominance subsampling
- `flags` (int): Encoding flags
- `dst` (buffer, optional): Pre-allocated destination buffer

**Returns:**
- `bytes`: JPEG encoded data

## Pixel Formats

- `TJPF_RGB` - RGB pixel order
- `TJPF_BGR` - BGR pixel order (OpenCV compatible)
- `TJPF_RGBA` - RGBA with alpha channel
- `TJPF_BGRA` - BGRA with alpha channel
- `TJPF_GRAY` - Grayscale

## Examples

### Batch Processing with DataLoader

```python
import torch
from torch.utils.data import Dataset, DataLoader
from turbojpeg import TurboJPEG, TJPF_RGB
from pathlib import Path

class JpegDataset(Dataset):
    def __init__(self, image_dir):
        self.files = list(Path(image_dir).glob('*.jpg'))
        self.jpeg = TurboJPEG()
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        with open(self.files[idx], 'rb') as f:
            # Decode directly to tensor
            img = self.jpeg.decode(f.read(), pixel_format=TJPF_RGB)
        # Convert to CHW format for PyTorch
        return img.permute(2, 0, 1).float() / 255.0

dataset = JpegDataset('/path/to/images')
loader = DataLoader(dataset, batch_size=32, num_workers=4)
```

### Fast Image Resizing

```python
from turbojpeg import TurboJPEG

jpeg = TurboJPEG()

# Use libjpeg-turbo's built-in scaling (faster than post-decode resize)
with open('large_image.jpg', 'rb') as f:
    # Scale to 1/2 size during decode
    img = jpeg.decode(f.read(), scaling_factor=(1, 2))
    
# Available scaling factors
print(jpeg.scaling_factors)
# frozenset({(1, 1), (1, 2), (1, 4), (1, 8), ...})
```

### Lossless Crop

```python
from turbojpeg import TurboJPEG

jpeg = TurboJPEG()

with open('input.jpg', 'rb') as f:
    jpeg_data = f.read()

# Lossless crop (x, y, width, height)
cropped = jpeg.crop(jpeg_data, 0, 0, 320, 240)

with open('cropped.jpg', 'wb') as f:
    f.write(cropped)
```

## Building Wheels

### Standard wheel

```bash
make wheel
```

### Bundled wheel (includes libjpeg-turbo)

```bash
# Linux (requires patchelf)
make install-patchelf
make bundle

# macOS
make bundle
```

The bundled wheel includes the libjpeg-turbo library, so users don't need to install it separately.

## Benchmark

Compared to PIL/Pillow and OpenCV:

| Operation | turbojpeg-torch | PIL | OpenCV |
|-----------|-----------------|-----|--------|
| Decode    | ~3x faster      | 1x  | ~2x    |
| Encode    | ~4x faster      | 1x  | ~2x    |

*Benchmarks on Intel i7, 1920x1080 JPEG images*

## License

MIT License - see LICENSE file for details.

Based on [PyTurboJPEG](https://github.com/lilohuang/PyTurboJPEG) by Lilo Huang, with PyTorch support added by Benjamin Paine.
