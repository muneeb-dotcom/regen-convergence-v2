# Project Log — regen-convergence-v2

## Day 2 — Data download

* GSE186527 (skin, scRNA-seq): 9 samples, mtx format
* GSE130438, GSE279540 (bulk RNA-seq): TPM/counts txt files

## Day 3 — QC

* 9 samples loaded, condition-labeled (PBS vs Verteporfin per paper)
* Filtered: >200 \& <6000 genes/cell, <10% mito → 7193 cells
* Doublets removed (Scrublet): 13 → 7180 cells final
* 2000 HVGs selected (seurat\_v3, on raw counts)

## Day 4 — Clustering \& pseudobulk

* PCA(30) + Leiden clustering → 28 clusters
* Annotated by marker genes: 13 fibroblast clusters (4046 cells), rest = immune/endothelial/keratinocyte/muscle/melanocyte
* Pseudobulk (fibroblasts only, summed raw counts): 19175 genes × 9 samples
* Saved: data/processed/skin\_pseudobulk\_counts.csv

## Day 5 — DESeq2 (skin fibroblasts, regenerative vs scarring)

* 3 vs 3 samples (POD7/14/30, Verteporfin vs PBS), baseline excluded
* Strict (padj<0.05,|LFC|>1) and relaxed (padj<0.1) both yield 1 gene: Plp1 (log2FC=-2.96, padj=0.0004)
* Low power expected with n=3/group — pivoting to full ranked gene list (7480 genes, by test stat) for Day 6 pathway/GSEA analysis instead of a fixed significance cutoff
* Files: skin\_DE\_strict.csv, skin\_DE\_relaxed.csv, skin\_DE\_ranked\_all\_genes.csv

## Day 6 — DESeq2 (digit P3, regenerating time course)

* GSE130438: 9 timepoints (0h,3h,6h,12h,24h,3d,7d,14d,21d), \~30 samples
* Part A (LRT, changes over time): 2499 genes, padj<0.05
* Part B (Wald, up vs 0h at any timepoint): ranged 28 (6h) to 222 (21d) genes
* Final set D3 (time-responsive AND up at some point): 418 genes
* File: digit\_P3\_regeneration\_responsive\_genes.csv

## Day 7 — DESeq2 (digit P2, non-regenerating time course)

* GSE279540 NR samples, 9 timepoints, \~29 samples
* Part A (LRT): 4410 genes change over time
* Part B (up vs 0h): peak at 14d (1798 genes — likely fibrotic/scarring signature)
* Final set D2: 1909 genes
* D2 >> D3 (1909 vs 418) — non-regenerating injury response is broader/more sustained
* D3\_specific (D3 - D2, regeneration-specific): 170 genes
* File: digit\_P2\_injury\_responsive\_genes.csv, digit\_regeneration\_specific\_genes.csv

## Day 8 — Convergence: skin vs digit regeneration

* S = top 200 skin genes by |DESeq2 stat| (exploratory, since strict list = 1 gene)
* D3\_specific = 170 digit regeneration-specific genes (Day 7)
* Raw overlap: 4 genes — Dusp4, Nfatc1, Saa3, Sfrp4
* Alias-corrected (org.Mm.eg.db, catches synonyms like Gja1/Cx43): still 4 genes, no additions
* File: convergent\_genes.csv / convergent\_genes\_alias\_corrected.csv

## Day 9 — Pathway enrichment convergence
* \- Enrichr (GO\_BP\_2023, KEGG\_2019\_Mouse, Reactome\_2022), padj<0.05
* \- Skin (S, top 200): 97 significant terms
* \- Digit (D3\_specific, 170 genes): 130 significant terms
* \- Shared: 12 terms — ECM organization/collagen biosynthesis, PI3K-Akt signaling,
* &#x20; cell migration regulation, inflammatory/granulocyte response, bone development
* \- File: shared\_pathway\_terms.csv
* \- Interpretation: pathway-level convergence stronger/more interpretable than
* &#x20; gene-level (4 genes) — suggests shared regenerative programs act via different
* &#x20; genes but same underlying biological processes
* 
* \## Day 9.5 — Figures
* \- volcano\_skin.png, geneset\_sizes.png, venn\_convergence.png saved to results/figures/

