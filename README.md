# Regen-Convergence

Computational search for convergent transcriptional signatures between two mouse regeneration systems: skin wound healing (scarring vs. YAP-inhibition-induced regeneration) and digit tip amputation (regenerating P3 vs. non-regenerating P2).

Full write-up: [`docs/regen_convergence_writeup_v3.docx`](docs/regen_convergence_writeup_v3.docx)

## Key Finding

Two evidence branches, kept separate:

- **Branch A (data-driven, 4 genes):** Dusp4, Nfatc1, Saa3, Sfrp4. These genes rank highly in skin AND are specific to digit regeneration. Two of them (Nfatc1, Sfrp4) have independently published roles in wound regeneration.
- **Branch B (pathway-driven, 108 genes):** genes underlying 12 shared enriched pathways (ECM organization, PI3K-Akt signaling), forming a denser STRING network (457 edges). Contains one gap junction gene, Gja1 (Cx43).

## Important Caveat

The skin dataset (GSE186527) has only 3 pooled libraries per group, each pooling multiple mice. All skin-side statistics are therefore reported as descriptive rankings, not significance tests. See the write-up, "Statistical framing" section.

## Datasets

| ID | Tissue | Role |
|---|---|---|
| GSE186527 | Mouse skin wound | Scarring vs. regenerative (descriptive) |
| GSE130438 | Mouse digit tip (P3) | Regenerating time course |
| GSE279540 | Mouse digit tip (P2) + macrophages | Non-regenerating time course; macrophage validation |

## Repository Structure

```text
regen-convergence-v2/
├── data/processed/     # cleaned counts, metadata, feature matrices
├── results/
│   ├── de_tables/      # differential expression outputs, both branches
│   ├── enrichment/     # pathway enrichment (Enrichr)
│   ├── network/        # STRING centrality, ion channel flags
│   ├── ml/             # classifier performance, permutation tests, SHAP
│   ├── figures/        # all plots
│   └── literature/     # PubMed counts, manual tiers
├── scripts/            # numbered by project day (day4, day5, ... day29)
├── docs/               # full write-up
└── PROGRESS.md         # day-by-day log
```

## Reproducing

Environment: conda, R (DESeq2, apeglm) and Python (scanpy, pandas, scikit-learn, shap, gseapy, mygene, GEOparse). Scripts run in day-number order; see `PROGRESS.md` for the exact sequence and the outputs of each step.

## Limitations

See the write-up's "Limitations" section. In summary:

- Small sample sizes throughout.
- The skin dataset is structurally limited to 3 pooled libraries per group.
- ML results are split into pre-registered (4-gene, non-significant) and exploratory (155-gene, significant but unvalidated), and are not equally weighted.
- Findings are correlational only, with no causal claims.
