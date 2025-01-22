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
econ_df.drop("2021\nLangzeitarbeitslosenquote (%)", axis=1, inplace=True)

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
#econ_df["2021\nAnteil 65- bis 79-J�hrige (%)"] = econ_df["2021\nAnteil 65- bis 79-J�hrige (%)"]
# TODO: Convert to float!!!
# econ_df["2021\nAnteil 65- bis 79-J�hrige (%)"] = econ_df["2021\nAnteil 65- bis 79-J�hrige (%)"].replace(",", ".")
# econ_df["2021\nAnteil ab 80-J�hrige (%)"] = econ_df["2021\nAnteil ab 80-J�hrige (%)"].replace(",", ".")
econ_df["2021\nAnteil ab 65-J�hrige (%)"] = econ_df["2021\nAnteil 65- bis 79-J�hrige (%)"] + econ_df["2021\nAnteil ab 80-J�hrige (%)"]

cols = econ_df.columns

econ_df = econ_df[list(set(econ_df.columns).difference(set(["2021\nAnteil ab 80-J�hrige (%)", "2021\nAnteil 65- bis 79-J�hrige (%)", "2021\nKaufkraft (Euro/Haushalt)"])))]
econ_df


# %%
# normalize the factors
for col in econ_df.columns:
    if "2021" not in col:
        continue
    econ_df[f"{col}_normalized"] = econ_df[col] / econ_df[col].max()

econ_df["socio_economic_index"] = econ_df["2021\nHaushalte mit niedrigem Einkommen (%)_normalized"] + econ_df["2021\nAnteil ab 65-J�hrige (%)_normalized"] + econ_df["2021\nVerschuldung im Kernhaushalt (Euro je Einwohner:in)_normalized"] - econ_df["2021\nAllgemeine Deckungsmittel (Euro je Einwohner:in)_normalized"]

# %%
econ_df["socio_economic_index"]

# %%
econ_df.to_csv("data/socioeconomic_factors_new.csv")


