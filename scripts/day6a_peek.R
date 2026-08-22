f1 <- read.delim("data/raw/GSE130438/suppl_https/GSE130438_ExpectCounts_Raw.txt.gz", nrows = 5)
cat("=== GSE130438 columns ===\n")
print(colnames(f1))

f2 <- read.delim("data/raw/GSE279540/suppl_https/GSE279540_Mouse_digit_ExpectCounts_.txt.gz", nrows = 5)
cat("\n=== GSE279540 digit columns ===\n")
print(colnames(f2))