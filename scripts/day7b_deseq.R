library(DESeq2)

counts_P2 <- read.csv("data/processed/digit_P2_counts.csv", row.names = 1)
coldata_P2 <- read.csv("data/processed/digit_P2_metadata.csv", row.names = 1)

coldata_P2$timepoint <- factor(coldata_P2$timepoint,
  levels = c("0h","3h","6h","12h","24h","3d","7d","14d","21d"))

dds_P2 <- DESeqDataSetFromMatrix(countData = round(counts_P2), colData = coldata_P2, design = ~ timepoint)
dds_P2 <- dds_P2[rowSums(counts(dds_P2) >= 10) >= 3, ]

# Part A: does this gene change at all across the timeline?
dds_P2_lrt <- DESeq(dds_P2, test = "LRT", reduced = ~ 1)
res_P2_lrt <- results(dds_P2_lrt, alpha = 0.05)
timepoint_responsive <- rownames(res_P2_lrt)[!is.na(res_P2_lrt$padj) & res_P2_lrt$padj < 0.05]
cat("Time-responsive genes (LRT):", length(timepoint_responsive), "\n")

# Part B: does it specifically go UP at any point vs. 0h?
dds_P2_wald <- DESeq(dds_P2, test = "Wald")
tp_list <- c("3h","6h","12h","24h","3d","7d","14d","21d")
up_in_any_tp <- c()
for (tp in tp_list) {
  r <- lfcShrink(dds_P2_wald, contrast = c("timepoint", tp, "0h"), type = "ashr")
  up <- rownames(r)[!is.na(r$padj) & r$padj < 0.05 & r$log2FoldChange > 1]
  up_in_any_tp <- union(up_in_any_tp, up)
  cat(tp, "vs 0h - up:", length(up), "\n")
}

D2 <- intersect(timepoint_responsive, up_in_any_tp)
cat("Final injury-responsive set (D2):", length(D2), "\n")

write.csv(D2, "results/de_tables/digit_P2_injury_responsive_genes.csv")