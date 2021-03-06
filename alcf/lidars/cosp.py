import numpy as np
import ds_format as ds

WAVELENGTH = 1064 # nm
CALIBRATION_COEFF = 1.0
SURFACE_LIDAR = None
SC_LR = None

def read(filename, vars, **kwargs):
	d = ds.from_netcdf(filename, vars)
	return d

