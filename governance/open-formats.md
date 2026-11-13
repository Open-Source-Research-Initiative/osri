# Open formats for research exchange

Use this guidance with the shared contribution standards. Use formats that collaborators can inspect, exchange, and reuse with commonly available tools. Start with the defaults below and keep the native source when an export would lose scientific meaning or editability.

| Material | Practical default |
| --- | --- |
| Notes, protocols, and documentation | UTF-8 Markdown; export PDF when a fixed reading copy is useful. |
| Small tables | UTF-8 CSV with a data dictionary or schema. |
| Larger typed tables | Parquet with a dictionary and the reader/library version; offer a small CSV example when useful. |
| Structured records and exchanges | JSON; JSONL for one record per line. Include a schema when fields need validation. |
| Human-edited configuration | YAML or JSON, with the supported version and an example. |
| References | BibTeX, RIS, or CSL JSON, retaining DOI or other stable identifiers. |
| Figures and diagrams | Editable source and SVG where suitable; PNG for raster images and PDF for fixed publication copies. |

CSV alone does not preserve field types or explain what values mean. Record column definitions, types, units, missing-value codes, date formats and time zones, identifiers, and relationships between tables. Preserve identifiers with leading zeros as strings. A short dictionary is enough for a simple table; [W3C CSV metadata](https://www.w3.org/TR/tabular-metadata/) provides a machine-readable option. [Parquet](https://parquet.apache.org/docs/file-format/types/) preserves typed fields but still needs descriptions of their meaning and origin.

Use domain formats when they preserve the research better than a general table. Examples include SBML or CellML for suitable biological models and FMI for supported model exchange or co-simulation. NetCDF or HDF5 can support suitable scientific arrays, and STEP can support CAD exchange. Keep the native model, solver inputs, coordinate systems, units, dependencies, and format versions needed to interpret or rerun it. Check an exchange export in the receiving tool before treating it as equivalent to its source.

## Keep the source and its history

Retain editable sources beside reading copies or link them through a versioned manifest. Record the source version, transformation script or export settings, software version, and any lost information. A spreadsheet may remain an editable working source. Export its exchange tables and retain the formulas and transformations needed to reproduce them. A PDF or screenshot alone is usually insufficient for reusable data or a model.

Keep small, shareable sources, schemas, scripts, and metadata in Git. Put large artifacts and restricted material in appropriate external storage. Track a shareable manifest containing artifact IDs, versions, locations, checksums where appropriate, provenance, access conditions, and regeneration instructions. Keep confidential paths and metadata in the controlled record when necessary.

An open format does not make its contents open data. State the license or access terms separately, preserve attribution, and check what may be shared. Use the [resource request process](resource-requests.md) when access requires an administrator. These defaults supplement the [contribution standards](contribution-standards.md); projects can document a better format for their methods.
