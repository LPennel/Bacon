import pandas as pd
import numpy as np

print("Running...1\n")

df = pd.read_csv("name.basics.tsv", sep="\t")

df = df.drop(columns=["birthYear", "deathYear"])

df = df.replace(r"\N", np.nan)
df = df.dropna()

df.to_csv("actors.csv", index=False)

print("Running...2\n")

df = pd.read_csv("title.basics.tsv", sep="\t")

df = df.drop(columns=["endYear"])

df = df.replace(r"\N", np.nan)

df = df.dropna()

df.to_csv("Titles.csv", index=False)
