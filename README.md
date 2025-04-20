# Document Resizer & Converter

A collection of Python utilities to prepare images and PDFs for upload to Indian government portals (visa, passport applications, etc.) by resizing, compressing, and converting documents to meet strict file size and dimension requirements.

## Features

- **Image Resize & Compress**: Resize photos to exactly 160×(200–212) pixels and compress to 5–20 KB.
- **PDF Compression**: Compress any PDF to under 100 KB using Ghostscript’s `/screen` preset.
- **PDF-to-JPG Conversion**: Convert multi-page PDFs into a single vertical JPEG under 100 KB using PyMuPDF and Pillow.

## Prerequisites

- **Python** 3.7 or newer
- **pip** (Python package installer)
- **Ghostscript** (required for PDF compression)
- **Poppler** (optional; only if you use the `pdf2image` approach)

### Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y ghostscript poppler-utils
```

#### macOS (Homebrew)
```bash
brew install ghostscript poppler
```

#### Windows
1. Download and install Ghostscript from [https://www.ghostscript.com/download/gsdnld.html](https://www.ghostscript.com/download/gsdnld.html) and ensure `gs` is in your PATH.  
2. (Optional) Download Poppler for Windows from a trusted source and add its `bin` folder to your PATH.

## Installation

Clone the repository and install Python dependencies:

```bash
git clone https://github.com/<your-username>/document-resizer-converter.git
cd document-resizer-converter
python3 -m venv venv
source venv/bin/activate       # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Image Resize & Compress
Resize a photo to 160×212 px and compress to ≤ 20 KB:

```bash
python resize_and_compress_image.py
```
- Prompts for the image path.  
- Outputs `<original_basename>_resized.jpg` in the same directory.

### 2. PDF Compression
Compress a PDF to ≤ 100 KB using Ghostscript’s `/screen` preset:

```bash
python compress_screen.py
```
- Prompts for the PDF path.  
- Outputs `<original_basename>_compressed.pdf`.

### 3. PDF-to-JPG Conversion
Convert a multi-page PDF into one concatenated JPEG (≤ 100 KB):

```bash
python convert_pdf_to_jpg.py
```
- Prompts for the PDF path.  
- Outputs `<original_basename>_combined.jpg`.

## Files in This Project

| Script                         | Description                                      |
|--------------------------------|--------------------------------------------------|
| `resize_and_compress_image.py` | Image resizing + compression (160×212 px, ≤ 20 KB) |
| `compress_screen.py`           | PDF compression (≤ 100 KB, `/screen` preset)      |
| `convert_pdf_to_jpg.py`        | Convert PDF pages to one JPEG (≤ 100 KB)          |
| `requirements.txt`             | Python dependencies                               |

## Requirements File

```text
pillow
pymupdf
# pdf2image  # Only if you choose the Poppler-based converter
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or issue in the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

