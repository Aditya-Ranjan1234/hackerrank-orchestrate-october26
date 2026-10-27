"""Generate a page/row-level source inventory for PDFs and text handovers."""
from pathlib import Path

try:
    from .pdf_inspector import inspect_pdf
except ImportError:
    from pdf_inspector import inspect_pdf


def write_report(root):
    root=Path(root)
    lines=["# PDF and plain-text evidence inventory", "",
           "Text and table cells below come directly from the supplied files. A page-level co-mention does not prove that every resource on the page belongs to every named person. Extracted audit facts still require a selected single-subject document or an exact row/trace join.", ""]
    for path in sorted((root/"dataset/evidence").rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".pdf",".txt"}:
            continue
        rel=path.relative_to(root).as_posix()
        lines.extend([f"## {rel}",""])
        if path.suffix.lower()==".txt":
            value=path.read_text(encoding="utf-8-sig",errors="replace")
            lines.extend([f"Plain-text lines: {len(value.splitlines())}.","","```text",value.rstrip(),"```",""])
            continue
        result=inspect_pdf(path)
        lines.extend([f"Pages: {result['page_count']}; scanned pages: {sum(page['scanned'] for page in result['pages'])}.",""])
        for page in result["pages"]:
            lines.extend([f"### Page {page['page']}","",f"Text characters: {page['text_length']}; tables: {page['table_count']}.","", "```text",page["text"].rstrip(),"```",""])
            for number,table in enumerate(page["tables"],1):
                lines.extend([f"Table {number}, {len(table)} rows:","", "```text"])
                lines.extend(" | ".join(str(cell or "").replace("\n"," / ") for cell in row)
                             for row in table)
                lines.extend(["```",""])
    target=root/"code/evaluation/document_text_inventory.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return target


if __name__=="__main__":
    print(write_report(Path(__file__).resolve().parents[2]))
