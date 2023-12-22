# Code to recalculate units inside ERA5 files.
# Created by Vit Kovacka on 2023-12-20
# CAFL Aon Impact Forecasting project


import os
import xarray as xr

# Get the list of files in the directory
file_list = os.listdir("V:/Canada/ERA5/Frazer/")

# Iterate over the files
for file_name in file_list:
    if file_name.startswith("Fraser_") and file_name.endswith(".nc"):
        # Open the NetCDF file
        data = xr.open_dataset(os.path.join("V:/Canada/ERA5/Frazer/", file_name))

        # Convert the variable from m/day to mm/day
        data["ro"] *= 1000
        data["ro"].attrs["units"] = "mm"

        # Save the modified dataset to a new NetCDF file
        output_file = file_name.replace(".nc", "_mm.nc")
        data.to_netcdf(os.path.join("V:/Canada/ERA5/Frazer/", output_file))
