"""Inspect PDF text and tables page by page; do not infer owner from headers."""
from pathlib import Path


def inspect_pdf(path):
    import pdfplumber
    pages = []
    with pdfplumber.open(Path(path)) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            tables = page.extract_tables() or []
            pages.append({"page": number, "text": text, "text_length": len(text),
                          "tables": tables, "table_count": len(tables),
                          "scanned": len(text.strip()) < 50})
    return {"page_count": len(pages), "pages": pages,
            "notes": ["scanned, needs Vision"] if any(p["scanned"] for p in pages) else []}
