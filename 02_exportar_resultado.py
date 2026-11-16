import pandas as pd, glob, csv
partes = sorted(glob.glob("actores_parts/part-*"))
df = pd.concat([pd.read_csv(p, sep="\t", header=None, names=["actor","cantidad_titulos"],
                encoding="utf-8", keep_default_na=False, quoting=csv.QUOTE_NONE)
                for p in partes])
df = df.sort_values(["cantidad_titulos","actor"], ascending=[False, True])
df.to_csv("mapreduce_actores.csv", index=False, encoding="utf-8")
print(len(df)); print(df.head(10))