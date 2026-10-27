import re
import hashlib
from datetime import datetime
EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE = re.compile(r"(?<!\w)\+?[0-9][0-9 ()-]{6,}[0-9](?!\w)")
def email_hashes(identity):
    """Exact SHA-256 aliases of known current/historical emails, without Phase 1 mutation."""
    explicit={str(v).casefold() for v in getattr(identity,"all_email_hashes",())}
    derived={hashlib.sha256(str(email).strip().casefold().encode("utf-8")).hexdigest()
             for email in getattr(identity,"all_emails",())}
    return explicit | derived
def dt(value):
    if not value: return None
    try: return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError: return None
def hit(path, value, kind, row=None, page=None):
    return {"field_path": path, "value_kind": kind, "value": value.casefold() if kind == "email" else value, "source_row": row, "source_page": page}
def hits(text, path="text", known=(), row=None, page=None):
    out=[]
    for m in EMAIL.findall(text): out.append(hit(path, m, "email", row, page))
    for m in PHONE.findall(text): out.append(hit(path, m.strip(), "phone", row, page))
    for uid in known:
        if uid in text: out.append(hit(path, uid, "user_id", row, page))
    return out
