# Medical Quick Reference Generator

A Python-based document generation system that transforms a JSON dataset of medicines into a polished, print-ready PDF handbook.

## Features
- **Offline Generation**: No web frameworks or APIs required.
- **Print Optimized**: A4 portrait, page numbers, running footers, and orphan/widow control via CSS Paged Media.
- **Auto-generated**: Dynamic Table of Contents and Quick Reference cheat sheet.
- **No JS**: Pure HTML/CSS rendered to PDF.

## Prerequisites
- Python 3.8+
- [WeasyPrint dependencies](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) (varies by OS, e.g., Pango, Cairo)

## Installation

1. Create a virtual environment (optional but recommended):
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. Install the required Python packages:
```bash
    pip install Jinja2 WeasyPrint
```


## Usage

1. Add or edit medicines in `medicines.json`.
2. Run the generator:
```bash
    python generate.py
```
3. Check the `output/` folder for `medicine_guide.pdf` and `medicine_guide.html`.