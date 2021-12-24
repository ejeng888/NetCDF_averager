<h1>NetCDF averager</h1>

This script will calculate the atmospheric average for variables in a netCDF file(s).
<br />
To run the script:
<br />
   > . ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/
   > 
   > python netcdf_averager.py
<br />
If you encounter an error with the netCDF4 library, then run pip install netCDF4 in command line.

The script may not work the way you expect if running with vectors or cumulative variables such as precipitation

Note: config file must be in same directory as main script and must be named netcdf_averager_config
