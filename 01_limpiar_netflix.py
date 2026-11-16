import pandas as pd

df = pd.read_csv("netflix_titles.csv", dtype=str, keep_default_na=False, encoding="utf-8")
n_orig, n_cols = len(df), df.shape[1]

# 1-2. strip y saltos de línea/tabulaciones -> espacio
for c in df.columns:
    df[c] = df[c].str.strip().str.replace(r"[\r\n\t]+", " ", regex=True)
# 3. vacíos -> nulos
df = df.replace("", pd.NA)

# 4. duplicados completos
dup_full = int(df.duplicated().sum());           df = df.drop_duplicates()
# 5. sin show_id
sin_id = int(df["show_id"].isna().sum());        df = df[df["show_id"].notna()]
# 6. show_id repetido (se conserva el primero)
rep_id = int(df.duplicated("show_id").sum());    df = df.drop_duplicates("show_id", keep="first")

# 7. date_added -> dd/mm/aaaa
f = pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")
df["date_added"] = f.dt.strftime("%d/%m/%Y")

# 8. duration_min solo para Movie
mins = df["duration"].str.extract(r"(\d+)\s*min", expand=False)
df["duration_min"] = pd.to_numeric(mins.where(df["type"] == "Movie"), errors="coerce").astype("Int64")

# 11. guardar
df.to_csv("netflix_clean.csv", index=False, encoding="utf-8")

# 1.2 resultados (Tabla 1)
peli = df["type"] == "Movie"
con = int((peli & (df["duration_min"].fillna(0) > 0)).sum())
print("Registros originales:", n_orig)
print("Columnas originales:", n_cols)
print("Duplicados completos eliminados:", dup_full)
print("Sin show_id eliminados:", sin_id)
print("show_id repetido eliminados:", rep_id)
print("Registros limpios:", len(df))
print("Películas con duration_min > 0:", con)
print("Películas sin duración > 0:", int(peli.sum()) - con)