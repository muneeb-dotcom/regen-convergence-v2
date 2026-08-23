from Bio import Entrez
import time, pandas as pd

Entrez.email = "muneebshahzadshakeelahmad@gmail.com"

def pubmed_count(gene, context_terms=("regeneration", "wound healing", "digit tip")):
    context = " OR ".join(f'"{t}"[Title/Abstract]' for t in context_terms)
    term = f'("{gene}"[Title/Abstract]) AND (Mus musculus[Organism]) AND ({context})'
    handle = Entrez.esearch(db="pubmed", term=term, retmax=0)
    record = Entrez.read(handle)
    handle.close()
    time.sleep(0.34)
    return int(record["Count"])

convergent = pd.read_csv("results/de_tables/convergent_genes.csv")["gene"].tolist()
counts = {g: pubmed_count(g) for g in convergent}
print(counts)

pd.Series(counts, name="pubmed_count").to_csv("results/literature/pubmed_counts.csv")