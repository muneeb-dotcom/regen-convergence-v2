library(org.Mm.eg.db)
library(AnnotationDbi)

S <- rownames(read.csv("results/de_tables/skin_DE_ranked_all_genes.csv", row.names = 1))
ranked <- read.csv("results/de_tables/skin_DE_ranked_all_genes.csv", row.names = 1)
ranked$abs_stat <- abs(ranked$stat)
S <- rownames(ranked[order(-ranked$abs_stat), ])[1:200]

D3_specific <- read.csv("results/de_tables/digit_regeneration_specific_genes.csv")[,1]

canonical <- function(genes) {
  sym <- suppressWarnings(AnnotationDbi::select(org.Mm.eg.db, keys = genes, keytype = "ALIAS", columns = "SYMBOL"))
  out <- setNames(sym$SYMBOL, sym$ALIAS)
  ifelse(genes %in% names(out), out[genes], genes)
}

S_canon <- unique(canonical(S))
D3_canon <- unique(canonical(D3_specific))

convergent_canon <- sort(intersect(S_canon, D3_canon))
cat("Convergent (alias-corrected):", length(convergent_canon), "\n")
print(convergent_canon)

write.csv(convergent_canon, "results/de_tables/convergent_genes_alias_corrected.csv", row.names = FALSE)