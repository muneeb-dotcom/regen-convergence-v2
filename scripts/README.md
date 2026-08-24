# Regen-Convergence

Computational search for convergent transcriptional signatures between two mouse regeneration systems: skin wound healing (scarring vs YAP-inhibition-induced regeneration) and digit tip amputation (regenerating P3 vs non-regenerating P2).

Full write-up: `docs/regen_convergence_writeup_v2.docx`

## Key finding

Two evidence branches, kept separate:

- **Branch A (data-driven, 4 genes):** Dusp4, Nfatc1, Saa3, Sfrp4 — genes ranking highly in skin AND specific to digit regeneration. Two (Nfatc1, Sfrp4) have independently published roles in wound regeneration.
- **Branch B (pathway-driven, 108 genes):** genes underlying 12 shared enriched pathways (ECM organization, PI3K-Akt signaling). Denser STRING network (457 edges). Contains one gap junction gene, Gja1 (Cx43).

## Important caveat

Skin dataset (GSE186527) has only 3 pooled libraries per group (each pooling multiple mice). All skin-side statistics are reported as descriptive rankings, not significance tests. See write-up, "Statistical framing" section.

## Datasets

| ID | Tissue | Role |
|---|---|---|
| GSE186527 | Mouse skin wound | Scarring vs regenerative (descriptive) |
| GSE130438 | Mouse digit tip (P3) | Regenerating time course |
| GSE279540 | Mouse digit tip (P2) + macrophages | Non-regenerating time course; macrophage validation |

## Structure