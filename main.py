import numpy as np
import pandas as pd
from netCDF4 import Dataset
import xarray as xr
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from rasterstats import zonal_stats




climat = Dataset('data/klima_gridded.nc', mode='r')
hotdays = climat['hetaja']
long = climat['lon']
lat = climat['lat']



shapefile_path = 'data/kommunen_shape.shp'
shapes = gpd.read_file(shapefile_path)


lon_min, lon_max = np.min(long), np.max(long)
lat_min, lat_max = np.min(lat), np.max(lat)
resolution = (long[1] - long[0], lat[1] - lat[0])


transform = from_origin(lon_min, lat_max, resolution[0], resolution[1])

print('b')
with rasterio.open(
    "temp_raster.tif",
    "w",
    driver="GTiff",
    height=hotdays.shape[1],
    width=hotdays.shape[2],
    count=1,
    dtype=hotdays.dtype,
    crs="EPSG:4326",  # WGS84 projection
    transform=transform,
) as dst:
    dst.write(hotdays[0], 1)  # Write the first time step
print('a')
stats = zonal_stats(
    shapefile_path,  # Path to your shapefile
    "temp_raster.tif",  # Path to your raster
    stats=["mean", "max", "min"]  # Statistics to calculate
)
print('c')
shapes['hotdays'] =[stat['mean'] for stat in stats]
shapes.plot(column="mean_temperature", cmap="coolwarm", legend=True)
plt.title("Mean Temperature by Region")
plt.show()
