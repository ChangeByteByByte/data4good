import xarray as xr
import rioxarray

def convert_netcdf_to_utm32n(input_file, output_file):
    """
    Convert NetCDF data from geographic coordinates to EPSG:25832 (UTM Zone 32N)
    
    Parameters:
    input_file (str): Path to input NetCDF file
    output_file (str): Path to save the converted NetCDF file
    """
    try:
        # Open the dataset
        ds = xr.open_dataset(input_file)
        
        # Ensure the dataset has spatial coordinates
        if 'longitude' not in ds.coords and 'lat' not in ds.coords:
            raise ValueError("Dataset must contain longitude and latitude coordinates")
            
        # Assign the original CRS (assuming WGS 84)
        ds.rio.write_crs("EPSG:4326", inplace=True)
        
        # Check if coordinates are within the specified bounds
        lon_min, lon_max = 5.83333, 15.16667
        if (ds.longitude < lon_min).any() or (ds.longitude > lon_max).any():
            raise ValueError(f"Longitude values must be between {lon_min} and {lon_max}")
        
        # Reproject to UTM Zone 32N
        ds_utm = ds.rio.reproject(
            dst_crs="EPSG:25832",
            resolution=1000,  # Resolution in meters, adjust as needed
            resampling=rioxarray.enums.Resampling.bilinear
        )
        
        # Add CRS attributes to the output file
        ds_utm.attrs['crs'] = 'EPSG:25832'
        ds_utm.attrs['crs_wkt'] = ds_utm.rio.crs.to_wkt()
        
        # Save the reprojected dataset
        ds_utm.to_netcdf(output_file)
        
        return True
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False
    
    finally:
        # Ensure proper cleanup
        try:
            ds.close()
            ds_utm.close()
        except:
            pass

# Example usage
if __name__ == "__main__":
    input_file = "input.nc"
    output_file = "output_utm32n.nc"
    
    success = convert_netcdf_to_utm32n(input_file, output_file)
    if success:
        print("Conversion completed successfully")
    else:
        print("Conversion failed")