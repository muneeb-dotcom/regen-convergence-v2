# Project Log — regen-convergence-v2

## Day 2 — Data download
- GSE186527 (skin, scRNA-seq): 9 samples, mtx format
- GSE130438, GSE279540 (bulk RNA-seq): TPM/counts txt files

## Day 3 — QC (skin scRNA-seq)
- 9 samples loaded, condition-labeled (PBS=scarring vs Verteporfin=regenerative per paper)
- Filtered: >200 & <6000 genes/cell, <10% mito -> 7193 cells
- Doublets removed (Scrublet): 13 -> 7180 cells final
- 2000 HVGs selected (seurat_v3, on raw counts)

## Day 4 — Clustering & pseudobulk
- PCA(30) + Leiden clustering -> 28 clusters
- Annotated by marker genes: 13 fibroblast clusters (4046 cells), rest = immune/endothelial/keratinocyte/muscle/melanocyte
- Pseudobulk (fibroblasts only, summed raw counts): 19175 genes x 9 samples
- File: data/processed/skin_pseudobulk_counts.csv

## Day 5 — DESeq2 (skin fibroblasts, regenerative vs scarring)
- 3 vs 3 samples (POD7/14/30, Verteporfin vs PBS), baseline excluded
- Strict (padj<0.05,|LFC|>1) and relaxed (padj<0.1): both yield 1 gene — Plp1 (log2FC=-2.96, padj=0.0004)
- Low power expected with n=3/group — pivoted to full ranked gene list (7480 genes, by test stat)
- Files: skin_DE_strict.csv, skin_DE_relaxed.csv, skin_DE_ranked_all_genes.csv

## Day 6 — DESeq2 (digit P3, regenerating time course)
- GSE130438: 9 timepoints (0h,3h,6h,12h,24h,3d,7d,14d,21d), ~30 samples
- Part A (LRT, changes over time): 2499 genes, padj<0.05
- Part B (Wald, up vs 0h at any timepoint): ranged 28 (6h) to 222 (21d) genes
- Final set D3 (time-responsive AND up at some point): 418 genes
- File: digit_P3_regeneration_responsive_genes.csv

## Day 7 — DESeq2 (digit P2, non-regenerating time course)
- GSE279540 NR samples, 9 timepoints, ~29 samples
- Part A (LRT): 4410 genes change over time
- Part B (up vs 0h): peak at 14d (1798 genes — likely fibrotic/scarring signature)
- Final set D2: 1909 genes
- D2 >> D3 (1909 vs 418) — non-regenerating injury response is broader/more sustained
- D3_specific (D3 - D2, regeneration-specific): 170 genes
- Files: digit_P2_injury_responsive_genes.csv, digit_regeneration_specific_genes.csv

## Day 8 — Convergence: skin vs digit regeneration
- S = top 200 skin genes by |DESeq2 stat| (exploratory, since strict list = 1 gene)
- D3_specific = 170 digit regeneration-specific genes (Day 7)
- Raw overlap: 4 genes — Dusp4, Nfatc1, Saa3, Sfrp4
- Alias-corrected (org.Mm.eg.db, catches synonyms like Gja1/Cx43): still 4 genes, no additions
- Files: convergent_genes.csv, convergent_genes_alias_corrected.csv

## Day 9 — Pathway enrichment convergence
- Enrichr (GO_BP_2023, KEGG_2019_Mouse, Reactome_2022), padj<0.05
- Skin (S, top 200): 97 significant terms
- Digit (D3_specific, 170 genes): 130 significant terms
- Shared: 12 terms — ECM organization/collagen biosynthesis, PI3K-Akt signaling, cell migration regulation, inflammatory/granulocyte response, bone development
- File: shared_pathway_terms.csv
- Interpretation: pathway-level convergence stronger/more interpretable than gene-level (4 genes) — suggests shared regenerative programs act via different genes but same underlying biological processes

## Day 9.5 — Figures
- volcano_skin.png, geneset_sizes.png, venn_convergence.png saved to results/figures/

## Day 11 — STRING network (4 convergent genes)
- Threshold 400: zero edges
- Threshold 150: one edge, Sfrp4-Nfatc1 (score 0.209, low confidence)
- Files: string_centrality.csv, string_centrality_lowconf.csv

## Day 12 — GO ion channel flagging (4 convergent genes)
- Checked against GO ion channel/gap junction/pump terms
- Zero matches (automated + manual name check)
- File: ion_channel_flags.csv

## Day 13 — Feature matrix + macrophage validation
- Built skin_sample_metadata.csv (condition labels)
- Feature matrix: 4 genes, z-scored per dataset, 65 total samples (33 regen, 32 non-regen)
- Extra: macrophage validation (GSE279540 M1/M2/baseline) — all 4 genes significant M2 vs M1
  (Dusp4, Sfrp4 up in M2; Nfatc1, Saa3 down in M2)
- Files: ml_feature_matrix_X.csv, ml_feature_matrix_y.csv, macrophage_convergent_genes_M2vM1.csv

## Day 14 — ML models (LOOCV, 4-gene set)
- logreg: acc 0.26, AUC 0.15
- rf: acc 0.65, AUC 0.66 (best)
- mlp: acc 0.52, AUC 0.51
- File: loocv_performance.csv

## Day 15-16 — Permutation test + expanded gene set
- 4-gene RF model: p=0.078 (not significant)
- Expanded to 155-gene set (D3_specific x all 3 datasets): RF acc 0.85, AUC 0.91, p=0.020 (significant)
- Labeled as exploratory/secondary, not pre-registered
- Files: permutation_test.csv, ml_feature_matrix_X_expanded.csv, permutation_test_expanded.csv

## Day 16 — SHAP (4-gene RF model)
- Saa3 most influential (0.140), then Nfatc1 (0.049), Dusp4 (0.040), Sfrp4 (0.031)
- Files: shap_gene_ranking.csv, shap_summary.png

## Day 17 — PubMed counts (4 convergent genes)
- Dusp4: 4, Nfatc1: 57, Saa3: 3, Sfrp4: 7
- File: pubmed_counts.csv

## Day 18 — Literature tiers (4 convergent genes, manual review)
- Nfatc1: Known regulator (wound healing NFAT signaling)
- Sfrp4: Known regulator (direct fibrotic vs regenerative Wnt control, Gay et al. Sci Adv 2020)
- Saa3: Studied elsewhere (inflammation/immunity)
- Dusp4: Studied elsewhere (MAPK signaling, cancer/cardiac)
- File: literature_tiers.md

## Day 19 — Final evidence table (4-gene, first version)
- Combined DE stats, STRING, GO flags, SHAP, PubMed, literature tier
- File: final_evidence_table.csv

## Day 20 — First write-up + GitHub setup
- Created repo: https://github.com/muneeb-dotcom/regen-convergence-v2
- Pushed clean history (raw data excluded via .gitignore)
- First write-up drafted (v1)

## Day 21 — GEO label verification (enhancement phase start)
- Confirmed via GEO series summary: Verteporfin = YAP inhibition = regeneration; PBS = scarring
- PMID 35077667, matches original labeling — no relabeling needed

## Day 22 — Unused replicate search
- Confirmed GSE186527 is the only scRNA-seq deposit for this study (checked paper text)
- No additional mouse skin replicates publicly available
- GSE219158 exists but is a large-animal (pig) study, not usable
- Conclusion: n=3 pooled libraries/group is a hard ceiling

## Day 23 — Descriptive relabeling (skin stats)
- Renamed padj column throughout: "padj_descriptive_only"
- Added explicit note: not a validated significance test, ranking only
- File: skin_DE_ranked_DESCRIPTIVE.csv

## Day 24 — Ion channel screen (merged branches)
- Screened 111 genes: 4 convergent (Branch A) + 108 ECM/signaling (Branch B)
- 1 hit: Gja1 (Cx43) — gap junction channel, GO:0005243, GO:0005921
- File: ion_channel_flags_MERGED.csv, branch_b_ecm_signaling_genes.csv

## Day 25 — Figure fixes
- volcano_skin.png had a bug (invalid negative -log10 values) — fixed
- geneset_sizes.png, venn_convergence.png, shap_summary.png verified correct, no fix needed
- File: volcano_skin_FIXED.png

## Day 26 — Merged evidence table (Branch A + B)
- 111 genes, tagged by branch (A_convergent / B_ecm_signaling)
- File: final_evidence_table_MERGED.csv

## Day 27 — STRING network (111-gene merged list)
- 457 edges (score>=400) — much denser than 4-gene network
- Top hubs: Fn1(46), Ptprc(36), Cxcr4(30), Icam1(27), Spp1(26)
- File: string_centrality_MERGED.csv

## Day 28 — PubMed counts (111-gene merged list)
- Automated counts, all 111 genes
- Top hits: Bcl2(499), Myc(469), Cxcr4(327), Bmp4(161), Icam1(105)
- File: pubmed_counts_MERGED.csv

## Day 29 — Write-up rewrite (v2, then v3)
- v2: descriptive framing applied throughout, ion channel section added, both branches
  shown separately, fixed volcano figure inserted
- v3 fix: extended manual literature tiering from 4 genes to top 20 (by STRING degree +
  SHAP) plus Branch A = 23 genes total. 8/23 known regulators (incl. Bmp4, Col2a1, Col9a2
  — digit bone/cartilage regeneration), 15/23 studied elsewhere
- Added explicit caveat: raw PubMed counts biased toward generically famous genes
- Files: literature_tiers_TOP20.csv, docs/regen_convergence_writeup_v3.docx

## Day 30 — Repo cleanup, final push
- README rewritten (initially saved empty by mistake — fixed after audit)
- Write-up v3 in docs/, all Day 21-29 outputs committed and pushed
- Project complete