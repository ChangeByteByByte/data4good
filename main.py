import numpy as np
import pandas as pd
from netCDF4 import Dataset
import xarray as xr
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from rasterstats import zonal_stats
# from convert_crs import convert_netcdf_to_utm32n as convert_crs
import os


climat = pd.read_csv('data/data_morgenpost.csv')
com = pd.read_csv('data/communen.csv', sep=';')

print(min(climat['ags']), max(climat['ags']))
print(min(com['GKZ']), max(com['GKZ']))

com['ags'] = com['GKZ']
com['ags'] = com['ags'] / 1000
com['ags'] = com['ags'].astype(int)

rename_col = {'HI': 'Heat', 'ET': 'Ice', 'SU': 'HDays', 'TN' : 'HNight', 'DD' : 'DryDays', 'R20mm' : 'Rain'}
