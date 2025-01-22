import pandas as pd
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import locale


df = pd.read_csv('data/Bevölkerungsanteil - Frauen und Bevölkerungsanteil - Männer für kreisfreie Städte und Landkreise.csv', sep=';')
cols = [c for c in df.columns if 'Bevölkerungsanteil' in c]
for c in cols:
    df[c] = df[c].str.replace(',', '.').astype(float)

years = ['2020', '2025', '2030', '2040']
pairs = ['Bevölkerungsanteil - Männer (%)', 'Bevölkerungsanteil - Frauen (%)']
lst = [y + '\nBevölkerungsanteil - Frauen (%)' for y in years]
lst.append('GKZ')

df_for_map = df[lst]
df_for_map['ags'] = df_for_map['GKZ'] // 1000


map = gpd.read_file('data/Shapefiles/shapefile.shp')
map['ags'] = map['schluessel'].astype(int)

map = map.merge(df_for_map, on='ags')


def makemap(col=None, title=''):
    map.plot(column=col, figsize=(6, 8), edgecolor="black", legend=True).set_axis_off()
    plt.title(title)
    # plt.show()


for y in years:
    s = y + '\nBevölkerungsanteil - Frauen (%)'
    makemap(col=s, title=y)
plt.show()
