# Historical initial research contract — 2026-11-16

This initial contract is retained as historical evidence. The [active expansion contract](campaigns/2026-11-16-expansion/CONTRACT.md) supersedes its difficulty-rating and eligibility rules.

Build a broad, maintainable directory of free submission AND free publication opportunities across OSRI's existing scope. This is a venue catalog, not manuscript-specific matching. Five distinct agents are assigned to each of twelve initial subfield clusters, in five roles: discovery, diamond/open dissemination expansion, fee audit, ranking evidence, and skeptical review. Clusters are navigational coverage, not an exhaustive discipline taxonomy.

## Ownership and output

Work only in the role/subfield file assigned in the task. Use live web research, principally official author instructions, publisher policies, society pages, and official journal statistics. Save UTF-8 JSON. Do not edit shared canonical files. No secrets, installs, remote writes, or submissions. Any temporary research files must stay in this repository on `/workspace`.

Discovery and diamond outputs have `subfield`, `role`, `checked_on`, `records` (array), and `notes`. Each record uses this shape (unknown values are null or `unknown`, never guessed):

```json
{
  "id": "subfield-venue-slug",
  "name": "Full venue name",
  "kind": "journal",
  "publisher": "Publisher or institution",
  "homepage": "https://...",
  "author_guidelines": "https://...",
  "submission_url": null,
  "subjects": ["subfield-slug"],
  "formats": ["original_research", "review", "methods", "software", "data"],
  "scope_notes": "Specific computational, existing-data, synthesis or methodological work that fits; limitations.",
  "route": {
    "model": "diamond",
    "submission_fee": "none",
    "publication_fee": "none",
    "eligibility": "needs_verification",
    "oa_status": "open_access",
    "conditions": "Article type, length, optional costs, waiver/affiliation requirements, uncertainty.",
    "other_mandatory_costs": "none stated; verify if unclear",
    "fee_evidence": [{"url": "https://...", "checked_on": "2026-11-16", "note": "Short paraphrase of what this policy actually establishes.", "access": "page"}]
  },
  "review": {"type": "peer_reviewed", "source_urls": ["https://..."]},
  "difficulty": {"band": "unknown", "basis": "No ranking established yet.", "source_urls": []},
  "metrics": [],
  "discovery_sources": ["https://..."]
}
```

Allowed `kind`: journal, conference, preprint_server, repository, research_blog. Allowed route `model`: diamond, subscription, conditional_waiver, conditional_agreement, free_deposit, unknown. Allowed eligibility: verified_free, conditional, needs_verification, not_free. Allowed review type: peer_reviewed, editorial, moderation, none, unknown. `access`: page, search_snippet, blocked, unavailable. Fee values: none, charged, unknown. Difficulty bands: very_high, high, moderate, unknown, not_comparable. A band is an explicitly identified agent judgment, never measured acceptance odds.

Metrics are objects with `name`, `value`, `year`, `population` (e.g. submitted manuscripts vs externally reviewed manuscripts), `source_url`, and `note`. Use only officially reported values, their exact years and definitions. Missing metrics remain missing. Do not label journals easy from absent data, impact factor, or citation count. Do not rank different disciplines or preprints on a single prestige ladder.

Fee and ranking auditors write `{subfield, role, checked_on, patches: [{id, route?, difficulty?, metrics?, review?, formats?, scope_notes?, audit_note?}], notes}`. A supplied field replaces that field in the final merge. Preserve accurate evidence while correcting. Fee auditors inspect all records from discovery and diamond roles, and may add excluded leads to notes. Only call a route verified_free when official evidence covers submission and standard publication, without required payment or selective waiver. A generic publisher policy is evidence only when its applicability to this journal and route is established. Unknown compulsory costs mean needs_verification. Mandatory conference registration means not_free unless a documented unconditional free route exists.

Reviewers read discovery, diamond, fee and ranking files and write `{subfield, role, checked_on, patches: [...], findings: [{id, severity, issue, resolution}], notes}`. Challenge weak fee evidence, stale/uncited numbers, incorrect peer review, scope mismatch and unsupported ranking. Make concrete corrective patches, including demotion to needs_verification or unknown. Independent agent review is not human scientific or usability review.

## Roles

1. Discovery: find 8–10 credible journal venues (at least 6 if evidence is sparse). Prefer diversity and verifiable zero-cost routes; retain important paid counterexamples only as explicitly not_free or conditional.
2. Diamond/open expansion: read discovery; find 3–5 additional diamond journals, regional/society/university outlets, or genuinely free research-software/data venues. Add at most two relevant free preprint/repository routes, labeled accurately. Avoid duplicates. Document exclusions where useful.
3. Fees: independently audit every candidate, including submission, standard publication, page/length, compulsory membership/registration, OA and conditional waivers. Conservative eligibility beats a larger recommended list.
4. Ranking: collect official metrics for the journals that disclose them, with period/denominator. Suggest reasoned within-subfield difficulty bands only where evidenced by editorial selectivity, contribution criteria or acceptance statistics. Citation impact alone cannot establish acceptance difficulty; unknown is valid. Read the fee audit if present but work independently.
5. Review: inspect merged implications and challenge mistakes; verify a sample plus every suspicious claim. State what was actually checked.

Keep final chat reports brief: output path, number of records or patches, and material caveats. The files are the deliverable.
