"""Classify request intent with bounded word stems."""
import re

DELETION_STEM_PATTERNS=[
    r"\bdelet\w*\b",r"\bremov\w*\b",r"\beras\w*\b",r"\b(?:forget|forgot)\w*\b",
    r"\bpurg\w*\b",r"\bdestroy\w*\b",r"\banonymi[sz]\w*\b",r"\bterminat\w*\b",
    r"\bwip\w*\b",r"\bright to erasure\b",r"\bright to be forgotten\b",
    r"\bclose my account\b",r"\bclose the account\b",r"\bclose account\b",
    r"\bpermanently delete\b",r"\bpermanently remove\b",r"\bdeletion\b",
    # The request stream includes Portuguese account-erasure requests.  Their
    # instruction to verify identifiers must not turn the deletion into an
    # access/verification-only request.
    r"\bexclu(?:s[aã]o|ir)\w*\b",r"\belimina(?:ç[aã]o|ci[oó]n|r)\w*\b",
    r"\bsupress(?:ion|ão|ao)\w*\b",
]
NON_DELETION_STEM_PATTERNS=[
    r"\bexport\w*\b",r"\bdownload\w*\b",r"\bview\w*\b",r"\baccess\w*\b",
    r"\bverif\w*\b",r"\bupdat\w*\b",r"\bchang\w*\b",r"\bcorrect\w*\b",
    r"\bamend\w*\b",r"\bmodif\w*\b",r"\bedit\w*\b",r"\bunsubscribe\b",
    r"\bopt[\s-]?out\b",r"\bstop receiving\b",r"\bstop emails\b",
    r"\b(?:merge|split)\w*\b",r"\btransfer ownership\b",
]
_DELETION_REGEX=[re.compile(p,re.I) for p in DELETION_STEM_PATTERNS]
_NON_DELETION_REGEX=[re.compile(p,re.I) for p in NON_DELETION_STEM_PATTERNS]

# Scope and negation matter more than the mere occurrence of "delete".  These
# patterns describe request language, not case IDs or expected answers.
_NEGATED_PREFIX=re.compile(r"\b(?:not|never|without|don['’]t)\b[^.!?;]{0,90}$",re.I)
_LIMITED_MARKETING=re.compile(r"\b(?:marketing|promotional|mailing)\b",re.I)
_ACCOUNT_SCOPE=re.compile(r"\b(?:account|profile|personal\s+(?:data|information))\b",re.I)
_EXPLICIT_OTHER=re.compile(
    r"\b(?:replace|reset(?:ting)?|misspell\w*)\b|"
    r"\b(?:copy|information request|promotional emails|marketing lists)\b|"
    r"\b(?:leave|keep)\b.{0,60}\b(?:active|in place|as it is)\b",re.I)

def matched_keywords(text):
    value=(text or "").strip()
    return [m.group() for regex in _DELETION_REGEX+_NON_DELETION_REGEX if (m:=regex.search(value))]

def is_deletion_request(request_text):
    text=(request_text or "").strip()
    if not text: return True
    deletion=False
    rejected_scope=False
    for sentence in re.split(r"[.!?;]",text):
        for regex in _DELETION_REGEX:
            for match in regex.finditer(sentence):
                if _NEGATED_PREFIX.search(sentence[:match.start()]):
                    rejected_scope=True
                    continue
                if _LIMITED_MARKETING.search(sentence) and not _ACCOUNT_SCOPE.search(sentence):
                    rejected_scope=True
                    continue
                deletion=True
    non=(rejected_scope or bool(_EXPLICIT_OTHER.search(text))
         or any(r.search(text) for r in _NON_DELETION_REGEX))
    return not non or deletion
