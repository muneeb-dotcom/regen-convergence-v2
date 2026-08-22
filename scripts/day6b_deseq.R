library(DESeq2)

counts_P3 <- read.csv("data/processed/digit_P3_counts.csv", row.names = 1)
coldata_P3 <- read.csv("data/processed/digit_P3_metadata.csv", row.names = 1)

coldata_P3$timepoint <- factor(coldata_P3$timepoint,
  levels = c("0h","3h","6h","12h","24h","3d","7d","14d","21d"))

dds_P3 <- DESeqDataSetFromMatrix(countData = round(counts_P3), colData = coldata_P3, design = ~ timepoint)
dds_P3 <- dds_P3[rowSums(counts(dds_P3) >= 10) >= 3, ]

# Part A: does this gene change at all across the timeline?
dds_P3_lrt <- DESeq(dds_P3, test = "LRT", reduced = ~ 1)
res_P3_lrt <- results(dds_P3_lrt, alpha = 0.05)
timepoint_responsive <- rownames(res_P3_lrt)[!is.na(res_P3_lrt$padj) & res_P3_lrt$padj < 0.05]
cat("Time-responsive genes (LRT):", length(timepoint_responsive), "\n")

# Part B: does it specifically go UP at any point vs. 0h?
dds_P3_wald <- DESeq(dds_P3, test = "Wald")
tp_list <- c("3h","6h","12h","24h","3d","7d","14d","21d")
up_in_any_tp <- c()
for (tp in tp_list) {
  r <- lfcShrink(dds_P3_wald, contrast = c("timepoint", tp, "0h"), type = "ashr")
  up <- rownames(r)[!is.na(r$padj) & r$padj < 0.05 & r$log2FoldChange > 1]
  up_in_any_tp <- union(up_in_any_tp, up)
  cat(tp, "vs 0h - up:", length(up), "\n")
}

D3 <- intersect(timepoint_responsive, up_in_any_tp)
cat("Final regeneration-responsive set (D3):", length(D3), "\n")

dir.create("results/de_tables", recursive = TRUE, showWarnings = FALSE)
write.csv(D3, "results/de_tables/digit_P3_regeneration_responsive_genes.csv")