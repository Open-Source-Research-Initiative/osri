# Sources, access, and coverage

This catalog was assembled on 2026-11-15 from official repositories, documentation, author-associated code, publisher records, and DOI metadata. It is a curated starting inventory, not a systematic search or a census of all simulation software.

## What was checked

- Repository availability and source-license information were inspected for the listed tools. License summaries identify the core source where possible; dependency, data, plugin, and asset terms remain separate.
- Citation titles and DOIs were checked against Crossref. The bibliography records publication types and per-reference reading status. Metadata verification does not mean the article's methods were read or tested.
- The featured walkthroughs identify specific inspected code, paper passages, or upstream instructions. Only the four included CPU examples were executed here. The [verification record](verification.md) reports their results.

The broad catalog has more tools than application guides. Rows without a verified paper or local walkthrough say so. Adding a paper-linked example for those tools is an open contribution; a documentation link is not represented as a literature example.

## Restricted articles supplied for this work

Cole supplied Black and Scholes (1973), DOI [10.1086/260062](https://doi.org/10.1086/260062), and Carroll (1997), DOI [10.1162/003355397555109](https://doi.org/10.1162/003355397555109), from a personal library. The relevant assumptions, equations, and calibration passages were inspected locally. The PDFs, page images, and extracted full text are not included in this repository or the website.

The public resources contain citations, passage locations, independently written explanations, and teaching code. The [Carroll guide](examples/economics.md) records the difference between the original prose and later author-associated code rather than silently treating them as identical.

## Important distinctions

| Item | How it is represented |
| --- | --- |
| OpenUSD | Scene composition and exchange; TOST-1.0 source license. The custom battery attributes are an OSRI example, not a standard electrochemical schema. |
| Isaac Sim / Isaac Lab | Open-source components with separate runtime and asset terms. The guide pins a compatible historical pair. Orbit's article and Isaac Lab's tutorial are distinguished. |
| CARLA | MIT source with additional Unreal runtime and asset terms; not an entirely open dependency stack. |
| ABIDES | Original framework and historical dependencies. The distinct JPMorgan fork was archived when checked. |
| PyPSA-Eur | Modern small tutorial linked to a 2018 model paper; the current run is not asserted to reproduce the original results. |
| SUMO LuST | Author model originally validated on SUMO 0.26. New simulator versions need a documented port and comparison. |
| ViNoS | JOSS article reviewed; source-host access challenge prevented model inspection. Archive retrieval and model licensing remain pending. |
| Turek–Hron | Benchmark citation and current preCICE implementation checked; original numerical target tables still need review before a reproduction claim. |

Keep dated source checks when updating the catalog. A repository can move, an archive can become unavailable, and default branches or licenses can change. Follow a guide's pinned version when its commands depend on that version.

## Credits and review

Human direction: Cole / @ajhcs. Codex researched sources, drafted resources, implemented the teaching scripts and catalog, and performed the recorded technical checks. Cole authorized merging and publishing the lab after a final technical review; acceptance and release are tracked in [PR #11](https://github.com/Open-Source-Research-Initiative/osri/pull/11). Independent human scientific review has not been recorded. The public guides and code follow the hub's [licensing](../LICENSE.md); linked third-party material retains its own terms.
