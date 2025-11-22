# DOCX to Text Converter

A simple Python script to convert .docx files to plain text files.

## Installation

1. Install the required dependency:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install python-docx
```

## Usage

Run the script with the input .docx file and output .txt file paths:

```bash
python docx_to_txt.py input.docx output.txt
```

### Example

```bash
python docx_to_txt.py my_document.docx my_document.txt
```

## Features

- Extracts all text content from .docx files
- Preserves paragraph structure
- Saves output as UTF-8 encoded text file
- Provides feedback on conversion success

## Requirements

- Python 3.6 or higher
- python-docx library
