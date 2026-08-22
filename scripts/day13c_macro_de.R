library(DESeq2)

raw <- read.delim("data/raw/GSE279540/suppl_https/GSE279540_Macrophages_ExpectCounts.txt.gz")
counts <- raw[, 3:ncol(raw)]
rownames(counts) <- make.unique(as.character(raw$Gene.ID))

condition <- c("M1","M1","M1","M2","M2","M2","Baseline","Baseline","Baseline")
coldata <- data.frame(condition = condition, row.names = colnames(counts))
coldata$condition <- factor(coldata$condition, levels = c("Baseline","M1","M2"))

dds <- DESeqDataSetFromMatrix(countData = round(counts), colData = coldata, design = ~ condition)
dds <- dds[rowSums(counts(dds) >= 10) >= 3, ]
dds <- DESeq(dds)

res <- results(dds, contrast = c("condition", "M2", "M1"))

genes <- c("Dusp4","Nfatc1","Saa3","Sfrp4")
out <- as.data.frame(res[rownames(res) %in% genes, ])
print(out)

write.csv(out, "results/de_tables/macrophage_convergent_genes_M2vM1.csv")