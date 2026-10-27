"""Read SQLite-compatible SQL exports without mutating the source files."""
import re
import sqlite3
from pathlib import Path

OWNER_COLUMNS = {"user_id", "user_uuid", "userid", "customer_id", "account_id", "customer_reference", "subject_reference", "email", "customer_email", "requester_email", "owner_email", "contact_email", "billing_email", "shipping_email", "email_hash"}


def inspect_database(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    names = re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["`\[]?([\w]+)', text, re.I)
    result = {"tables": [], "notes": []}
    if not names:
        result["notes"].append("no schema")
        return result
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(text)
        for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            quoted = '"' + name.replace('"', '""') + '"'
            cols = [r[1] for r in db.execute(f"PRAGMA table_info({quoted})")]
            result["tables"].append({"name": name, "columns": cols,
                "row_count": db.execute(f"SELECT COUNT(*) FROM {quoted}").fetchone()[0],
                "ownership_columns": [c for c in cols if c.casefold() in OWNER_COLUMNS]})
    except sqlite3.Error as exc:
        result["notes"].append(f"sqlite load error: {type(exc).__name__}")
        result["tables"] = [{"name": n, "columns": [], "row_count": None, "ownership_columns": []} for n in names]
    finally:
        db.close()
    return result


def ownership_rows(path, identifiers):
    """Return exact identifier matches, never suffix/substring joins."""
    wanted = {str(v).casefold() for v in identifiers if v}
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(Path(path).read_text(encoding="utf-8", errors="replace"))
        out = []
        for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            quoted = '"' + name.replace('"', '""') + '"'
            cols = [r[1] for r in db.execute(f"PRAGMA table_info({quoted})")]
            owners = [c for c in cols if c.casefold() in OWNER_COLUMNS]
            for row in db.execute(f"SELECT * FROM {quoted}"):
                raw = dict(zip(cols, row))
                matches = [c for c in owners if raw[c] is not None and str(raw[c]).casefold() in wanted]
                if matches:
                    out.append({"table": name, "resource_id": str(raw.get("resource_id") or raw.get("id") or ""), "columns": matches, "row": raw})
        return out
    except sqlite3.Error:
        return []
    finally:
        db.close()
