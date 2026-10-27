"""Evaluation-only trace from each sample answer step to supplied sources."""

import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from .pipeline import load_datasets
from .residual_provenance import inventory_sources
from agent.evidence.handlers.common import email_hashes


SEMANTIC = ("phase", "system_id", "resource_id", "operation", "state")


def read_rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return {row["case_id"]: row for row in csv.DictReader(stream)}


def key(step):
    return tuple(step.get(field) for field in SEMANTIC)


def exact(value, text):
    if not value:
        return False
    pattern = r"(?<![\w@.+-])" + re.escape(value) + r"(?![\w@.+-])"
    return bool(re.search(pattern, text, re.I))


def occurrences(resource_id, refs, lines):
    return [(location, any(exact(ref, line) for ref in refs))
            for location, line in lines if exact(resource_id, line)]


def other_input_occurrences(resource_id, input_texts):
    """Find a full ID in participant CSV inputs, excluding answer templates."""
    return [name for name, body in input_texts.items() if exact(resource_id, body)]


def json_record_ownership(path, resource_id, refs):
    """Count record objects, including nested profile/document owner fields."""
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    owner_names = {"user_id", "user_uuid", "customer_reference",
                   "subject_reference", "email", "customer_email",
                   "user_email", "owner_email", "requester_email",
                   "email_hash", "email_sha256", "hashed_email"}
    found = []

    def has_owner(node):
        if isinstance(node, dict):
            return any(name.casefold() in owner_names and isinstance(value, str)
                       and any(value.casefold() == ref.casefold() for ref in refs)
                       for name, value in node.items()) or any(
                has_owner(value) for value in node.values())
        if isinstance(node, list):
            return any(has_owner(value) for value in node)
        return False

    def visit(node):
        if isinstance(node, dict):
            if str(node.get("resource_id") or node.get("id") or "") == resource_id:
                found.append(has_owner(node))
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(data)
    return len(found), sum(found)


def citation(step, refs, manifest, sources, activities):
    cite = step.get("evidence_id") or ""
    resource = step.get("resource_id") or ""
    if cite in manifest:
        path = manifest[cite]
        if path.casefold().endswith(".json"):
            full_path = Path(__file__).resolve().parents[2] / "dataset" / path
            identifier_count, owned_count = json_record_ownership(full_path, resource, refs)
            return path, identifier_count, owned_count
        matches = occurrences(resource, refs, sources.get(path, []))
        return path, len(matches), sum(owner for _, owner in matches)
    if cite in activities:
        row = activities[cite]
        return "dataset/system_activity.csv:" + cite, int(row["resource_id"] == resource), int(
            any(exact(ref, row.get("details", "")) for ref in refs))
    return cite or "empty", 0, 0


def timestamp(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def build_report(root, output_csv):
    root = Path(root)
    mine = read_rows(output_csv)
    gold = read_rows(root / "dataset/sample_output.csv")
    requests = read_rows(root / "dataset/sample_deletion_requests.csv")
    datasets = load_datasets(root)
    manifest = {row["file_id"]: row["file_path"] for row in datasets.manifest}
    sources = {name.removeprefix("dataset/"): lines
               for name, lines in inventory_sources(root)}
    other_inputs = {
        path.name: path.read_text(encoding="utf-8-sig", errors="replace")
        for path in sorted((root / "dataset").glob("*.csv"))
        if path.name not in {"sample_output.csv", "output.csv"}
    }
    activities = {row["activity_id"]: row for row in datasets.activities}
    totals = Counter()
    cases = []
    missing = []
    citation_diffs = []
    unsupported_citations = []
    ownerless_citations = []
    for case_id in sorted(gold):
        if case_id not in mine:
            continue
        request = requests[case_id]
        identity = datasets.resolver.resolve(request["email"], request["audit_at"])
        refs = set(identity.all_user_ids) | set(identity.all_emails) | email_hashes(identity)
        actual = json.loads(mine[case_id]["steps_json"] or "[]")
        expected = json.loads(gold[case_id]["steps_json"] or "[]")
        actual_keys = {key(step): step for step in actual}
        expected_keys = {key(step): step for step in expected}
        missing_keys = expected_keys.keys() - actual_keys.keys()
        extra_keys = actual_keys.keys() - expected_keys.keys()
        different_citations = [k for k in expected_keys.keys() & actual_keys.keys()
                               if expected_keys[k].get("evidence_id") != actual_keys[k].get("evidence_id")]
        totals.update(cases=1,
                      status_match=mine[case_id]["deletion_status"] == gold[case_id]["deletion_status"],
                      array_match=actual == expected,
                      missing=len(missing_keys), extra=len(extra_keys),
                      citation_difference=len(different_citations))
        cases.append((case_id, gold[case_id]["deletion_status"],
                      mine[case_id]["deletion_status"], len(expected), len(actual),
                      len(missing_keys), len(extra_keys), len(different_citations)))
        for k in sorted(missing_keys):
            step = expected_keys[k]
            rid = step.get("resource_id") or ""
            cited = citation(step, refs, manifest, sources, activities)
            elsewhere = [(name, location, owner)
                         for name, lines in sources.items()
                         for location, owner in occurrences(rid, refs, lines)]
            pre = [row for row in datasets.activities
                   if row.get("resource_id") == rid and timestamp(row.get("event_time"))
                   and timestamp(row["event_time"]) <= timestamp(request["audit_at"])]
            direct_activity = sum(any(exact(ref, row.get("details", ""))
                                      for ref in refs) for row in pre)
            reported = timestamp(request.get("reported_at"))
            nearest = (min(abs((reported - timestamp(row["event_time"])).total_seconds())
                           for row in pre) if reported and pre else None)
            missing.append((case_id, step, cited, elsewhere, len(pre),
                            direct_activity, nearest))
        for k in sorted(different_citations):
            expected_step = expected_keys[k]
            actual_step = actual_keys[k]
            citation_diffs.append((case_id, expected_step, actual_step,
                                   citation(expected_step, refs, manifest, sources, activities),
                                   citation(actual_step, refs, manifest, sources, activities)))
        for step in expected:
            cited_path, id_count, owner_count = citation(step, refs, manifest, sources, activities)
            if (step.get("evidence_id") or "") in manifest:
                totals["file_citation_without_literal_id"] += int(id_count == 0)
                totals["file_citation_without_same_line_owner"] += int(
                    id_count > 0 and owner_count == 0)
                if id_count == 0:
                    unsupported_citations.append((case_id, step["resource_id"],
                                                  step["evidence_id"], cited_path))
                elif owner_count == 0:
                    ownerless_citations.append((case_id, step["resource_id"],
                                                 step["evidence_id"], cited_path))

    lines = ["# Sample gold backtrace", "",
             "Evaluation only: the production agent never imports this module or reads sample answers. A cited source can provide wider context; the counts below test full resource IDs and exact user IDs, current/historical emails or email hashes within the same JSON record, SQL row, PDF table row or log line.", "",
             "## Summary", "",
             "Status: " + str(totals["status_match"]) + "/" + str(totals["cases"]) +
             "; exact parsed step arrays: " + str(totals["array_match"]) + "/" + str(totals["cases"]) +
             "; missing semantic steps: " + str(totals["missing"]) +
             "; extra semantic steps: " + str(totals["extra"]) +
             "; shared-step citation differences: " + str(totals["citation_difference"]) + ".", "",
             "## All cases", "",
             "| Case | Gold status | Agent status | Gold steps | Agent steps | Missing | Extra | Citation differences |",
             "|---|---|---|---:|---:|---:|---:|---:|"]
    lines.extend("| " + " | ".join(map(str, row)) + " |" for row in cases)
    lines += ["", "## Missing semantic steps and their source links", "",
              "| Case | Resource / operation | Gold citation | ID in cited source | Owner in cited record | ID elsewhere | Pre-audit activity | Activity direct owner | Nearest activity to reported time |",
              "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for case_id, step, cited, elsewhere, activity_count, direct_owner, nearest in missing:
        columns = [case_id, step["system_id"] + "/" + step["resource_id"] + " " + step["operation"],
                   step.get("evidence_id") or "empty", cited[1], cited[2],
                   len(elsewhere), activity_count, direct_owner,
                   str(round(nearest)) + "s" if nearest is not None else "n/a"]
        lines.append("| " + " | ".join(map(str, columns)) + " |")
    lines += ["", "### Full ID occurrences for missing steps", ""]
    for case_id, step, cited, elsewhere, _, _, _ in missing:
        located = ", ".join("dataset/" + name + ":" + place +
                            (" (same-line owner)" if owner else "")
                            for name, place, owner in elsewhere[:8])
        lines.append("- " + case_id + " " + step["resource_id"] +
                     "; cited " + cited[0] + "; " +
                     (located or "no literal occurrence in 94 evidence files"))
    lines += ["", "## Shared steps with different citations", "",
              "| Case | Resource / operation | Gold citation | Gold ID/owner hits | Agent citation | Agent ID/owner hits |",
              "|---|---|---|---:|---|---:|"]
    for case_id, gold_step, our_step, gold_cite, our_cite in citation_diffs:
        columns = [case_id, gold_step["resource_id"] + " " + gold_step["operation"],
                   gold_step.get("evidence_id") or "empty",
                   str(gold_cite[1]) + "/" + str(gold_cite[2]),
                   our_step.get("evidence_id") or "empty",
                   str(our_cite[1]) + "/" + str(our_cite[2])]
        lines.append("| " + " | ".join(columns) + " |")
    lines += ["", "## Citation interpretation", "",
              "- Gold file citations lacking the literal resource ID: " +
              str(totals["file_citation_without_literal_id"]) + ".",
              "- Gold file citations naming the ID without an owner in the same structured record: " +
              str(totals["file_citation_without_same_line_owner"]) + ".",
              "- Empty citation on an INCOMPLETE follow-up step is expected output syntax.",
              "- Reported time and nearby ownerless activity are contextual only; the production agent excludes reported time and reported status.",
              "- This report does not reveal the gold generator's internal reasoning. It records visible support and gaps.", ""]
    lines += ["", "### Gold file citations without a literal target in that file", "",
              "| Case | Resource ID | Cited file ID | Source |", "|---|---|---|---|"]
    lines.extend("| " + " | ".join(row) + " |" for row in unsupported_citations)
    lines += ["", "### Gold file citations with a target but no owner on its literal line/row", "",
              "For PDFs this scan does not resolve a multi-line page layout; the original page and surrounding table must be reviewed before declaring an ownership gap.", "",
              "| Case | Resource ID | Cited file ID | Source |", "|---|---|---|---|"]
    lines.extend("| " + " | ".join(row) + " |" for row in ownerless_citations)
    absent = [(cid, step["resource_id"]) for cid, step, _, elsewhere, _, _, _ in missing
              if not elsewhere]
    absent_everywhere = [(cid, resource) for cid, resource in absent
                         if not other_input_occurrences(resource, other_inputs)]
    ownerless = [(cid, step["resource_id"]) for cid, step, _, elsewhere, _, _, _ in missing
                 if elsewhere and not any(owned for _, _, owned in elsewhere)]
    lines += ["## What the individual files establish", "",
              "- case_01: the gold verification cites evidence_54, a failover-replica SQL file. Its four resource rows include account_005 and three unrelated accounts; account_001 does not occur. The account_001 deletion activity (activity_3342) has no subject identifier. Its time is 17 seconds before the request's reported time, which is a claim rather than an owner field.",
              "- case_03: evidence_94 lines 42-43 and activity_3852 name analytics_9406. The lookup key, customer reference, email, phone and email hash are all null. The source establishes an anonymous profile observation, but not a link to the requester.",
              "- case_04: evidence_56 contains analytics_901 with null user ID, email, phone and email hash. The gold account_004 ID appears neither in evidence nor in a pre-audit activity row. A direct subject-to-resource path is unavailable.",
              "- case_21: evidence_92 includes account_6440 as a 404 readback and analytics_5335 as a profile with null identifiers. Activities name both IDs, but their details provide no user identifier. The sample assigns both to case_21; the visible sources do not identify that owner.",
              "- case_24: evidence_92 was captured before the September 15 noon cutoff and directly names the account/search resources with the requester email. Evidence_02 repeats them in a bundle captured September 17. The agent now prefers the contemporaneous citation while retaining the later bundle's historical rows for state reconstruction.",
              "- Across all missing steps, " + str(len(absent)) + " full IDs have no occurrence in the 94 evidence files; " + str(len(ownerless)) + " appear without a same-line/row owner. Every original PNG was also visually reviewed; none displays a missing full ID overlooked by OCR. Four PDF files were scanned through text and table extraction.",
              "- Of the " + str(len(absent)) + " IDs missing from evidence, " + str(len(absent_everywhere)) + " also have no full-ID occurrence in any other participant input CSV (excluding sample_output.csv and blank output.csv): " + ", ".join(cid + "/" + resource for cid, resource in absent_everywhere) + ". The other " + str(len(absent) - len(absent_everywhere)) + " appear in system_activity.csv but have no direct user field. This is a literal-source inventory, not a claim that the gold answers are false.",
              "- The gold-free temporal probe found that the nearest account action to reported time belonged to the direct owner in only 71 of 212 evaluable full-dataset requests. Numeric account/user suffixes agreed in only 1 of 240 directly owned account resources. The agent therefore uses neither timing nor numeric suffixes to fill these gaps.", ""]
    target = root / "code/evaluation/sample_gold_backtrace.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, totals


if __name__ == "__main__":
    import sys
    workspace = Path(__file__).resolve().parents[2]
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else workspace / "artifacts/csv/phase17_log_schema_sample.csv"
    report, totals = build_report(workspace, output)
    print(str(totals["status_match"]) + "/" + str(totals["cases"]) +
          " statuses; " + str(totals["array_match"]) + "/" +
          str(totals["cases"]) + " exact arrays; " + str(report))
