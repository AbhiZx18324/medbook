"""
Medical Guide PDF Generator
Transforms structured JSON medicine data into a print-ready PDF handbook.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

# --- Configuration ---
ROOT_DIR = Path(__file__).parent
DATA_FILE = ROOT_DIR / "medicines.json"
OUTPUT_DIR = ROOT_DIR / "output"
TEMPLATE_FILE = "template.html"
STYLE_FILE = "style.css"

def load_data(filepath: Path) -> List[Dict[str, Any]]:
    """Loads and returns the medicine JSON data."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def group_by_category(medicines: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Groups medicines into a dictionary keyed by category."""
    grouped = defaultdict(list)
    for med in medicines:
        grouped[med.get("category", "Miscellaneous")].append(med)
    return dict(grouped)

def generate_quick_reference(medicines: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Extracts the first 'used_for' symptom and maps it to the brand name
    to create a dynamic Quick Reference cheat sheet.
    """
    quick_ref = []
    seen_symptoms = set()
    
    for med in medicines:
        if med.get("used_for"):
            primary_symptom = med["used_for"][0]
            if primary_symptom not in seen_symptoms:
                quick_ref.append({
                    "symptom": primary_symptom,
                    "medicine": med["brand"]
                })
                seen_symptoms.add(primary_symptom)
                
    # Sort alphabetically by symptom for easy scanning
    return sorted(quick_ref, key=lambda x: x["symptom"].lower())

def slugify(text: str) -> str:
    """Creates a simple URL/ID friendly string."""
    return text.lower().replace(" & ", "-").replace(" ", "-")

def main():
    # 1. Setup Output Directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 2. Load and Process Data
    medicines = load_data(DATA_FILE)
    if not medicines:
        return

    grouped_medicines = group_by_category(medicines)
    quick_ref = generate_quick_reference(medicines)
    
    # 3. Setup Jinja2 Environment
    env = Environment(loader=FileSystemLoader(ROOT_DIR))
    env.filters['slugify'] = slugify  # Add custom slugify filter for TOC anchors
    template = env.get_template(TEMPLATE_FILE)
    
    # 4. Render HTML
    html_content = template.render(
        grouped_medicines=grouped_medicines,
        quick_reference=quick_ref,
        generation_date=datetime.now().strftime("%B %d, %Y"),
        version="1.0"
    )
    
    html_output_path = OUTPUT_DIR / "medicine_guide.html"
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # 5. Generate PDF using WeasyPrint
    pdf_output_path = OUTPUT_DIR / "medicine_guide.pdf"
    css_path = ROOT_DIR / STYLE_FILE
    
    print("Generating PDF (this may take a few seconds)...")
    HTML(filename=str(html_output_path)).write_pdf(
        target=str(pdf_output_path),
        stylesheets=[CSS(filename=str(css_path))]
    )
    
    print(f"Success! PDF generated at: {pdf_output_path}")

if __name__ == "__main__":
    main()