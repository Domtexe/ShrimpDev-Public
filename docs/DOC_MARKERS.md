# DOC_MARKERS

- Updated: `2026-03-01T19:14:59`

## Marker-Konvention

- Marker werden von Docs-Tools genutzt, um Updates **stabil und marker-basiert** einzufügen.

- Format:

```md
<!-- AUTO:NAME -->
<!-- /AUTO:NAME -->
```

## Erwartete Marker je Dokument

- `docs/MasterRules.md`: `<!-- AUTO:MR_RULES -->` … `<!-- /AUTO:MR_RULES -->`
- `docs/FILE_MAP.md`: `<!-- AUTO:FILE_MAP -->` … `<!-- /AUTO:FILE_MAP -->`
- `docs/SHORTCODES.md`: `<!-- AUTO:SHORTCODES_CORE -->` … `<!-- /AUTO:SHORTCODES_CORE -->`
- `docs/PIPELINE.md`: `<!-- AUTO:PIPELINE_META -->` … `<!-- /AUTO:PIPELINE_META -->`

## Templates

- Falls Templates existieren, müssen die gleichen Marker enthalten sein.
