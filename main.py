import numpy as np
import pandas as pd
from netCDF4 import Dataset


dt = Dataset('ger_klima_rcp85_30_2011-2100_p50_grd.nc', mode='r')

# communen = pd.read_csv('commenendata/data.csv', sep=';')

# print(communen.head())
