import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify

# from convert_crs import convert_netcdf_to_utm32n as convert_crs

df = pd.read_csv('data/data_morgenpost.csv')
com = pd.read_csv('data/communen.csv', sep=';')

# print(min(df['ags']), max(df['ags']))
# print(min(com['GKZ']), max(com['GKZ']))
rlf = 7338
com['ags'] = com['GKZ']
com['ags'] = com['ags'] / 1000
com['ags'] = com['ags'].astype(int)

rename_col = {'HI': 'Heat', 'ET': 'Ice', 'SU': 'HDays',
    'TN': 'HNight', 'DD': 'DryDays', 'R20mm': 'Rain'}

cols = df.columns
cols = [c for c in cols if (
    (c[-4:] == 'near' or c[-3:] == 'obs') and '85' in c) or c == 'ags']
# print(cols)
df = df[cols]
near = [c for c in cols if 'near' in c and c != 'ET_rsp85_near']
obs = [c for c in cols if 'obs' in c and c != 'ET_rsp85_obs']
for c in near:
    # df[c] = abs(df[c])
    df[c+'_normalised'] = df[c] / df[c].abs().max()
near = [c+'_normalised' for c in near]
df['c_score'] = df[near].sum(axis=1)
df['c_score_normalised'] = (
    df['c_score'] - min(df['c_score'])) / (max(df['c_score']) - min(df['c_score']))

## codes for Hamburg and Berlin
berlin = 11000
hh = 2000
df[df['GKZ'] == berlin]['socio_economic_index_normalised']
df[df['GKZ'] == hh]['socio_economic_index_normalised']

df_for_map = df[['ags', 'c_score', 'c_score_normalised']]


map = gpd.read_file('data/Shapefiles/shapefile.shp')
map['ags'] = map['schluessel'].astype(int)

map = map.merge(df_for_map, on='ags')


def makemap(col=None, title='', cmap=None):
    map.plot(column=col, figsize=(6, 8),edgecolor="black", legend=False, cmap=cmap, scheme='EqualInterval', k=5).set_axis_off()
    # plt.title(title)
    # plt.show()
    # plt.savefig(f'img/{title}.svg', transparent=True)
    # plt.savefig(f'img/{title}.png', transparent=True)

# makemap(col='c_score', title='Climate Impact Indicator')


econ = pd.read_csv('data/socioeconomic_factors_new.csv', sep=',')
econ['socio_economic_index_normalised'] = (econ['socio_economic_index'] - min(econ['socio_economic_index'])) / (max(econ['socio_economic_index']) - min(econ['socio_economic_index']))
tmp = econ[econ['GKZ'] == berlin*1000]['socio_economic_index_normalised']
tmp = econ[econ['GKZ'] == hh*1000]['socio_economic_index_normalised']

econ=econ[['GKZ', 'socio_economic_index', 'socio_economic_index_normalised']]
econ['ags']=econ['GKZ'] // 1000

map=map.merge(econ, on='ags')
# print(map.columns)
map['investment'] = map['c_score_normalised'] + map['socio_economic_index_normalised']
# print(map.loc[map['investment'].idxmax()])
lst = list(map['investment'])
lst.sort()
plt.plot(range(len(lst)), lst, '.')
# plt.show()

corrolation=map['c_score'].corr(map['socio_economic_index'])
# print(corrolation)


makemap(col='socio_economic_index_normalised', title='socio', cmap='Purples')
makemap(col='c_score_normalised', title='climat', cmap='Reds' )
