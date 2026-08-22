raw <- read.delim("data/raw/GSE279540/suppl_https/GSE279540_Mouse_digit_ExpectCounts_.txt.gz")

nr_cols <- grep("^NR_", colnames(raw), value = TRUE)
counts <- raw[, nr_cols]
rownames(counts) <- make.unique(as.character(raw$Gene.ID))

timepoint <- sub("^NR_([0-9]+[hd])_.*", "\\1", nr_cols)
coldata <- data.frame(timepoint = timepoint, row.names = nr_cols)
print(table(coldata$timepoint))

write.csv(counts, "data/processed/digit_P2_counts.csv")
write.csv(coldata, "data/processed/digit_P2_metadata.csv")