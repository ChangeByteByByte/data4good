# %%
import pandas as pd

# %%
econ_df = pd.read_csv('data/socioeconomic_factors.csv', sep=";")

# %%
new_cols = [col for col in econ_df.columns if ("2021" in col or not "20" in col)]

# %%
econ_df = econ_df[new_cols]
econ_df

# %%
import numpy as np

# %%
econ_df.drop("2021\r\nLangzeitarbeitslosenquote (%)", axis=1, inplace=True)

# %%
for col in econ_df.columns:
    if "2021" not in col:
        continue
    try:
        # print(econ_df[col].str.replace(",", "."))
        econ_df[col] = econ_df[col].str.replace(",", ".").astype(float)
    except:
        print("column not string")

# %%
#econ_df["2021\r\nAnteil 65- bis 79-Jährige (%)"] = econ_df["2021\r\nAnteil 65- bis 79-Jährige (%)"]
# TODO: Convert to float!!!
# econ_df["2021\r\nAnteil 65- bis 79-Jährige (%)"] = econ_df["2021\r\nAnteil 65- bis 79-Jährige (%)"].replace(",", ".")
# econ_df["2021\r\nAnteil ab 80-Jährige (%)"] = econ_df["2021\r\nAnteil ab 80-Jährige (%)"].replace(",", ".")
econ_df["2021\r\nAnteil ab 65-Jährige (%)"] = econ_df["2021\r\nAnteil 65- bis 79-Jährige (%)"] + econ_df["2021\r\nAnteil ab 80-Jährige (%)"]

cols = econ_df.columns

econ_df = econ_df[list(set(econ_df.columns).difference(set(["2021\r\nAnteil ab 80-Jährige (%)", "2021\r\nAnteil 65- bis 79-Jährige (%)", "2021\r\nKaufkraft (Euro/Haushalt)"])))]
econ_df


# %%
# normalize the factors
for col in econ_df.columns:
    if "2021" not in col:
        continue
    econ_df[f"{col}_normalized"] = econ_df[col] / econ_df[col].max()

econ_df["socio_economic_index"] = econ_df["2021\r\nHaushalte mit niedrigem Einkommen (%)_normalized"] + econ_df["2021\r\nAnteil ab 65-Jährige (%)_normalized"] + econ_df["2021\r\nVerschuldung im Kernhaushalt (Euro je Einwohner:in)_normalized"] - econ_df["2021\r\nAllgemeine Deckungsmittel (Euro je Einwohner:in)_normalized"]

# %%
econ_df["socio_economic_index"]

# %%
econ_df.to_csv("data/socioeconomic_factors_new.csv")


