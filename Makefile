# turbojpeg-torch Makefile
# Build Python package for libjpeg-turbo with PyTorch support

PYTHON ?= python3

.PHONY: all build wheel bundle clean test help install dev-install

all: wheel

help:
	@echo "turbojpeg-torch build targets:"
	@echo "  make build   - Build the package in-place"
	@echo "  make wheel   - Build a wheel package"
	@echo "  make bundle  - Build wheel with bundled libjpeg-turbo library"
	@echo "  make test    - Run tests"
	@echo "  make clean   - Clean build artifacts"
	@echo "  make install - Install the package"

build:
	$(PYTHON) -m pip install -e .

wheel:
	$(PYTHON) -m build --wheel $(WHEEL_BUILD_ARGS)

bundle: wheel
	@echo "Bundling libjpeg-turbo library into wheel..."
	@for whl in dist/*.whl; do \
		$(PYTHON) bundle_libs.py "$$whl" -o dist/; \
	done
	@echo "Done! Bundled wheel is in dist/"

test:
	$(PYTHON) -c "from turbojpeg import TurboJPEG; print('Import successful')"
	@echo "Running basic decode/encode test..."
	$(PYTHON) -c "\
from turbojpeg import TurboJPEG, TJPF_RGB; \
import torch; \
jpeg = TurboJPEG(); \
# Create a simple test by encoding a tensor and decoding it back; \
img = torch.zeros((100, 100, 3), dtype=torch.uint8); \
img[:, :, 0] = 255;  # Red image; \
encoded = jpeg.encode(img, pixel_format=TJPF_RGB); \
decoded = jpeg.decode(encoded, pixel_format=TJPF_RGB); \
print(f'Encoded size: {len(encoded)} bytes'); \
print(f'Decoded shape: {decoded.shape}, dtype: {decoded.dtype}'); \
assert isinstance(decoded, torch.Tensor), 'Expected torch.Tensor'; \
print('All tests passed!');"

clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/
	rm -rf turbojpeg_libs/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

install:
	$(PYTHON) -m pip install .

# Development install
dev-install:
	$(PYTHON) -m pip install -e .

# Install patchelf if needed for bundling on Linux
install-patchelf:
	@which patchelf > /dev/null 2>&1 || (echo "Installing patchelf..." && sudo apt-get install -y patchelf)

