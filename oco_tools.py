#!/usr/bin/env python
from glob import glob
import h5py
from netCDF4 import num2date
import numpy as np
import traceback

dict_oco2_xco2 = {
   #'variable_name': 'standard_name_from_netcdf',
    'lat': 'latitude',
    'lon': 'longitude',
	'sza': 'solar_zenith_angle',
    'vza': 'sensor_zenith_angle',
    'saa': 'Sounding/solar_azimuth_angle',
    'vaa': 'Sounding/sensor_azimuth_angle',
    'xco2': 'xco2',
    'xco2_sigma': 'xco2_uncertainty',
    'xco2_qual': 'xco2_quality_flag',
    'time': 'time'
}

class OCO2:
	def __init__(self, path, dictionary=dict_oco2_xco2, latMin=-90, latMax=90,lonMin=-180,lonMax=180):
		files = glob(path)
		# Check whether data has been initialized
		nini = True
		print('found', len(files), 'files')
		counter = 0
		totalcounter = 0
		for file in files:
			h = h5py.File(file,'r')
			try:
				# print('opening file', file)
				lat = h[dictionary['lat']][:]
				lon = h[dictionary['lon']][:]
				xco2_qual = h[dictionary['xco2_qual']][:]
				# print ('num soundings in file', len(lat))
				totalcounter+= len(lat)
				# filter on lat/lon
				isaoi = (lat>=latMin)&(lat<=latMax)&(lon>=lonMin)&(lon<=lonMax)&(xco2_qual==0)
				n = len(np.where(isaoi)[0])
				# print('num soundings in file aoi', n)
				counter+=n
				# print('total num soundings in aoi ', counter, ' total', totalcounter, ' % match', (counter/totalcounter*100))
				if nini and n>0:
					for k,v in dictionary.items():
						setattr(self, k, h[v][isaoi])
					nini = False
				elif n>0:
					for k,v in dictionary.items():
						temp = np.hstack((getattr(self, k), h[v][isaoi]))
						setattr(self, k, temp)
				h.close()
			except:
				print(traceback.format_exc())
				print('error opening file ', file)
				h.close()
		
		print('total num soundings in aoi ', counter, ' total', totalcounter, ' % match', (counter/totalcounter*100))
				

# Converts times in t_unit (string) and calendar t_cal (string) to a python datetime
def convert_time(nctime, t_unit, t_cal):
	datevar = []
	datevar.append(num2date(nctime,units = t_unit,calendar = t_cal))
	return datevar[0]


# Empty class (mimics Matlab structure capabilities)
class Timeseries:
    pass
	
# Creates a running mean of data
def running_mean(time_in, var_in, time_out, dTime):

	# Am lazy here, just creating an ordinal timestamp first (units of days)
	time_in_ord = np.asarray([x.toordinal() for x in time_in])
	time_out_ord = np.asarray([x.toordinal() for x in time_out])
	var_out = Timeseries()
	var_out.time = time_out
	# save a couple of statistics here:
	var_out.mean = np.zeros((len(time_out),))
	var_out.median = np.zeros((len(time_out),))
	var_out.perc90 = np.zeros((len(time_out),))
	var_out.perc10 =np.zeros((len(time_out),))
	var_out.std =np.zeros((len(time_out),))
	var_out.n =np.zeros((len(time_out),))
	var_out.standard_error =np.zeros((len(time_out),))
	
	for it in range(len(time_out_ord)):
		t = time_out_ord[it]
		wo = np.where(np.abs(time_in_ord-t)<dTime)[0]
		if len(wo)>1:
			var_out.mean[it]=np.mean(var_in[wo])
			var_out.median[it] =np.median(var_in[wo])
			var_out.perc90[it] =np.percentile(var_in[wo],90)
			var_out.perc10[it] =np.percentile(var_in[wo],10)
			var_out.std[it]    =np.std(var_in[wo])
			var_out.n[it] =len(wo)
			# This is trained on data, not the theoretical one:
			var_out.standard_error[it] = np.std(var_in[wo])/np.sqrt(len(wo))
		else:
			var_out.mean[it]=np.nan
			var_out.median[it] =np.nan
			var_out.perc90[it] =np.nan
			var_out.perc10[it] =np.nan
			var_out.std[it]    =np.nan
			var_out.n[it] =len(wo)
			# This is trained on data, not the theoretical one:
			var_out.standard_error[it] = np.nan

	
	return var_out
