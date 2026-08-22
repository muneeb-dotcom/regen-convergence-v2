library(DESeq2)

counts <- read.csv("data/processed/skin_pseudobulk_counts.csv", row.names = 1)

condition_map <- c(
  "GSM5429653_T1" = "baseline",
  "GSM5429654_T2" = "baseline",
  "GSM5429655_T3" = "baseline",
  "GSM5429656_T.7P" = "scarring",
  "GSM5429657_T.7V" = "regenerative",
  "GSM5429658_T.14P" = "scarring",
  "GSM5429659_T.14V" = "regenerative",
  "GSM5429660_T.30P" = "scarring",
  "GSM5429661_T.30V" = "regenerative"
)

coldata <- data.frame(condition = condition_map[colnames(counts)])
rownames(coldata) <- colnames(counts)

keep_samples <- coldata$condition != "baseline"
counts <- counts[, keep_samples]
coldata <- coldata[keep_samples, , drop = FALSE]
coldata$condition <- factor(coldata$condition, levels = c("scarring", "regenerative"))

print(coldata)

dds <- DESeqDataSetFromMatrix(countData = round(counts), colData = coldata, design = ~ condition)
dds <- dds[rowSums(counts(dds) >= 10) >= 3, ]
dds <- DESeq(dds)
res <- lfcShrink(dds, coef = "condition_regenerative_vs_scarring", type = "apeglm")
res_unshrunk <- results(dds, contrast = c("condition", "regenerative", "scarring"))
ranked <- as.data.frame(res_unshrunk)
ranked <- ranked[!is.na(ranked$stat), ]
ranked <- ranked[order(-ranked$stat), ]
write.csv(ranked, "results/de_tables/skin_DE_ranked_all_genes.csv")
cat("Ranked gene list saved:", nrow(ranked), "genes\n")

full <- as.data.frame(res)

sig_strict <- full[!is.na(full$padj) & full$padj < 0.05 & abs(full$log2FoldChange) > 1, ]
sig_relaxed <- full[!is.na(full$padj) & full$padj < 0.1, ]

dir.create("results/de_tables", recursive = TRUE, showWarnings = FALSE)
write.csv(sig_strict, "results/de_tables/skin_DE_strict.csv")
write.csv(sig_relaxed, "results/de_tables/skin_DE_relaxed.csv")

cat("Strict (padj<0.05, |LFC|>1):", nrow(sig_strict), "genes\n")
cat("Relaxed (padj<0.1):", nrow(sig_relaxed), "genes\n")
print(head(sig_relaxed[order(sig_relaxed$padj), ], 20))