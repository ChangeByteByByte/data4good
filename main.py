import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
# from convert_crs import convert_netcdf_to_utm32n as convert_crs

df = pd.read_csv('data/data_morgenpost.csv')
com = pd.read_csv('data/communen.csv', sep=';')

print(min(df['ags']), max(df['ags']))
print(min(com['GKZ']), max(com['GKZ']))

com['ags'] = com['GKZ']
com['ags'] = com['ags'] / 1000
com['ags'] = com['ags'].astype(int)

rename_col = {'HI': 'Heat', 'ET': 'Ice', 'SU': 'HDays', 'TN' : 'HNight', 'DD' : 'DryDays', 'R20mm' : 'Rain'}

cols = df.columns
cols = [c for c in cols if ((c[-4:] == 'near' or c[-3:] == 'obs') and '85' in c) or c == 'ags']
# print(cols)
df = df[cols]
near = [c for c in cols if 'near' in c and c != 'ET_rsp85_near']
obs = [c for c in cols if 'obs' in c and c != 'ET_rsp85_obs']
for c in near:
    # df[c] = abs(df[c])
    df[c+'_normalised'] = df[c] / df[c].abs().max()
near = [c+'_normalised' for c in near]
df['c_score'] = df[near].sum(axis=1)
# lst = list(df['c_score'])
# lst = [l for l in lst if not np.isnan(l)]
# lst.sort()
# plt.figure()
# plt.plot(range(len(lst)), lst, '.')
# plt.show()

df_for_map = df[['ags', 'c_score']]



map = gpd.read_file('data/Shapefiles/shapefile.shp')
map['ags'] = map['schluessel'].astype(int)

map = map.merge(df_for_map, on='ags')


def makemap(col=None, title=''):
    map.plot(column=col, figsize=(6, 8), edgecolor="black", legend=True).set_axis_off()
    plt.title(title)
    plt.savefig(f'img/{title}.svg', transparent=True)
    plt.savefig(f'img/{title}.png', transparent=True)

makemap(col='c_score', title='Climate Impact Indicator')
