import os
import pandas as pd
import numpy as np
import netCDF4 as nc
from configobj import ConfigObj


print("Starting")

config = ConfigObj(os.path.join(os.getcwd(), 'netcdf_averager_config'))
section1 = config['Main Variables']

directory = section1['directory']
save_path = section1['save_path']
os.makedirs(save_path, exist_ok = True)

section2 = config['Vars']
vars = section2['vars']
long_name = section2['long_name']
units = section2['units']

if((type(vars) != list) and (vars != '')):
    vars = [vars]
if((type(long_name) != list) and (long_name != '')):
    long_name = [long_name]
if((type(units) != list) and (units != '')):
    units = [units]

vars_dict = dict(zip(vars, zip(long_name, units)))
print(vars_dict)
if all(len(lst) == len(vars) for lst in [long_name, units]):
    if(len(vars) == 0):
        raise Exception("Length of one of the lists in ip1 variables is zero")
    print("All lists are same length")
else:
    raise Exception("Vars, ip1, average, and is_vector are not the same length")



def save_file(arr, save_path, xdim, ydim,  nomvar, vars_dict):
    print('Saving file')
    print(vars_dict.get(nomvar)[0])
    print(vars_dict.get(nomvar)[1])
    save_path = os.path.join(save_path,  nomvar + ".nc")
    print(save_path)
    if os.path.isfile(save_path):
        os.remove(save_path)
        
    ncfile = nc.Dataset(save_path, mode='w',format='NETCDF4_CLASSIC')
    ncfile.createDimension('lon', xdim)
    ncfile.createDimension('lat', ydim) 
    ncfile.createDimension('time', None)
    var = ncfile.createVariable(nomvar, np.float32, ('time','lon','lat'))
    var[:] = arr
    var.long_name = vars_dict.get(nomvar)[0]
    var.units = vars_dict.get(nomvar)[1]
    
    print(ncfile)
    ncfile.close()

for nomvar in vars:
    print("Now analyzing",  nomvar)
    averages_list = []
    i=0
    for fileName in sorted(os.listdir(directory)):
        the_file = os.path.join(directory, fileName)
        ds = nc.Dataset(the_file)
        array = ds[nomvar][:]
        averages_list.append(array)
        
        print("Finished analyzing file")
        i+=1
        #if(i==2):
            #break
            
    array = np.vstack(averages_list)
    array = np.mean(array, axis=0)
    xdim, ydim = array.shape
    save_file(array, save_path, xdim, ydim, nomvar, vars_dict)
    print("Finished saving",  nomvar)
    
    
print("Finished")
