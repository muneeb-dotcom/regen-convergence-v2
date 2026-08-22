raw <- read.delim("data/raw/GSE130438/suppl_https/GSE130438_ExpectCounts_Raw.txt.gz")

counts <- raw[, 3:ncol(raw)]
rownames(counts) <- raw$Gene.ID

sample_names <- colnames(counts)
timepoint <- sub("^Reg_([0-9]+[hd])_.*", "\\1", sample_names)

coldata <- data.frame(timepoint = timepoint, row.names = sample_names)
print(table(coldata$timepoint))

dir.create("data/processed", showWarnings = FALSE)
write.csv(counts, "data/processed/digit_P3_counts.csv")
write.csv(coldata, "data/processed/digit_P3_metadata.csv")