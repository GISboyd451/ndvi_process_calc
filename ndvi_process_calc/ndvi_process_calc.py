#
# Python 3.7
# Author: GISboyd451 (Contractor)
#
#

# I picked 'analysis ready data' in order to keep everything the same as what you have (or try to).
# Looks like I got some surface reflectance bands so I went ahead and used those since those have been corrected for sun angle, etc. (SB4, SB5, etc.)
# If surface reflectance is not available, we can use top of atmoshpere (TOA) I think.
# If neither of those are available, we will have to figure out a correction otherwise we would be using raw band values which (when calculating NDVI) will make our NDVI have a large error value.
#
# Here is how I would set this up:
#
import os
import sys
import numpy as np
import rasterio
from glob import glob
import pandas as pd 
import gdal

# Global output path (where do we want all our NDVI rasters to go):
f_path = 'T:/ProjectsNational/NationalDataQuality/Sprint/Alec_scripts/tia_ndvi/scenes/analysis_ready/combined_test'

# Combined test:
# Test to see if we can just throw everything into one location and then process.
try:
    os.chdir('T:/ProjectsNational/NationalDataQuality/Sprint/Alec_scripts/tia_ndvi/scenes/analysis_ready/combined_test')
    print("Folder found.")
except:
    print("Folder not found.")

#############################################################
#############################################################
# User controlled processing by typing in year (i.e. 2018)
# Change the directory to the year we want to process
# Get the year from user
# user_year = int(input("Input year: "))

# try:
#     os.chdir('T:/ProjectsNational/NationalDataQuality/Sprint/Alec_scripts/tia_ndvi/scenes/analysis_ready/%d' % user_year)
#     print("Folder found.")
# except:
#     print("Folder not found.")
##############################################################
##############################################################

# Get list of files by pattern
file_list = glob(os.path.join('*.tif'))

# Parse out the file names by character stripping, to get the satellite information from the Landsat file name.
satellite = list(map(lambda x: x[3], file_list))
processing = list(map(lambda x: x[5:7], file_list))
path = list(map(lambda x: x[8:11], file_list))
row = list(map(lambda x: x[11:14], file_list))
year = list(map(lambda x: x[15:19], file_list))
month = list(map(lambda x: x[19:21], file_list))
day = list(map(lambda x: x[21:23], file_list))
product_band = list(map(lambda x: x[-8:-4], file_list))
full_name = file_list

# Put all parsed out varaibles into a pandas dataframe 
user_database = pd.DataFrame(
    {'satellite':satellite,
    'prcoessing':processing,
    'path':path,
    'row':row,
    'year':year,
    'month':month,
    'day':day,
    'product_band':product_band,
    'full_name':full_name}
)
#

# Add in full date column
user_database["full_date"] = user_database["year"].map(str) + user_database["month"].map(str) + user_database["day"].map(str)

# Reorder database table
user_database = user_database.sort_values(by=['full_date', 'product_band'])
#print(user_database)

# Globally disable possible division by zero:
np.seterr(divide='ignore')

 # If the satellite is 8 (Landsat 8) then use the bands: 4 & 5 for ndvi
 # If the satellite is 7,5,4 (landsat) the use the bands: 3 & 4 for ndvi
 # If the satellite is 1,2,3 (landsat) then use the bands 4 & 6/7 for ndvi

for i, row in user_database.iterrows():
    sat_num = row['satellite']
    if str(sat_num) == '8':
        #pass landsat 8 logic
        band = row['product_band']
        if str(band) == 'SRB4':
            b4 = row['full_name']
            continue
        elif str(band) == 'SRB5':
            b5 = row['full_name']
            if b4[0:40] == b5[0:40]:
                print(b4)
                prefix = str(b4[0:40])
                print(b5)
                #ndvi calc
                print('ndvi calc')
                #import bands as separate 1 band raster
                band4 = rasterio.open(b4) #red
                band5 = rasterio.open(b5) #nir
                #generate nir and red objects as arrays in float64 format
                red = band4.read(1).astype('float64')
                nir = band5.read(1).astype('float64')
                #ndvi calculation, empty cells or nodata cells are reported as 0
                try:
                    ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))
                    ndvi[:5,:5]
                except:
                    print('Unable to process: '+ prefix)
                #export ndvi image
                ndviImage = rasterio.open(f_path+'/%s_ndvi.tif' % prefix,'w',driver='Gtiff', width=band4.width, height = band4.height, count=1, crs=band4.crs, transform=band4.transform, dtype='float64')
                ndviImage.write(ndvi,1)
                ndviImage.close()
    elif str(sat_num) == '7':
        #pass landsat 7 logic
        band = row['product_band']
        if str(band) == 'SRB3':
            b3 = row['full_name']
            continue
        elif str(band) == 'SRB4':
            b4 = row['full_name']
            if b3[0:40] == b4[0:40]:
                print(b3)
                prefix = str(b3[0:40])
                print(b4)
                #ndvi calc
                print('ndvi calc')
                #import bands as separate 1 band raster
                band3 = rasterio.open(b3) #red
                band4 = rasterio.open(b4) #nir
                #generate nir and red objects as arrays in float64 format
                red = band3.read(1).astype('float64')
                nir = band4.read(1).astype('float64')
                #ndvi calculation, empty cells or nodata cells are reported as 0
                try:
                    ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))
                    ndvi[:5,:5]
                except:
                    print('Unable to process: '+ prefix)
                #export ndvi image
                ndviImage = rasterio.open(f_path+'/%s_ndvi.tif' % prefix,'w',driver='Gtiff', width=band3.width, height = band3.height, count=1, crs=band3.crs, transform=band3.transform, dtype='float64')
                ndviImage.write(ndvi,1)
                ndviImage.close()
    elif str(sat_num) == '5':
        #pass landsat 5 logic
        band = row['product_band']
        if str(band) == 'SRB3':
            b3 = row['full_name']
            continue
        elif str(band) == 'SRB4':
            b4 = row['full_name']
            if b3[0:40] == b4[0:40]:
                print(b3)
                prefix = str(b3[0:40])
                print(b4)
                #ndvi calc
                print('ndvi calc')
                #import bands as separate 1 band raster
                band3 = rasterio.open(b3) #red
                band4 = rasterio.open(b4) #nir
                #generate nir and red objects as arrays in float64 format
                red = band3.read(1).astype('float64')
                nir = band4.read(1).astype('float64')
                #ndvi calculation, empty cells or nodata cells are reported as 0
                try:
                    ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))
                    ndvi[:5,:5]
                except:
                    print('Unable to process: '+ prefix)
                #export ndvi image
                ndviImage = rasterio.open(f_path+'/%s_ndvi.tif' % prefix,'w',driver='Gtiff', width=band3.width, height = band3.height, count=1, crs=band3.crs, transform=band3.transform, dtype='float64')
                ndviImage.write(ndvi,1)
                ndviImage.close()
    elif str(sat_num) == '4':
        #pass landsat 4 logic
        band = row['product_band']
        if str(band) == 'SRB3':
            b3 = row['full_name']
            continue
        elif str(band) == 'SRB4':
            b4 = row['full_name']
            if b3[0:40] == b4[0:40]:
                print(b3)
                prefix = str(b3[0:40])
                print(b4)
                #ndvi calc
                print('ndvi calc')
                #import bands as separate 1 band raster
                band3 = rasterio.open(b3) #red
                band4 = rasterio.open(b4) #nir
                #generate nir and red objects as arrays in float64 format
                red = band3.read(1).astype('float64')
                nir = band4.read(1).astype('float64')
                #ndvi calculation, empty cells or nodata cells are reported as 0
                try:
                    ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))
                    ndvi[:5,:5]
                except:
                    print('Unable to process: '+ prefix)
                #export ndvi image
                ndviImage = rasterio.open(f_path+'/%s_ndvi.tif' % prefix,'w',driver='Gtiff', width=band3.width, height = band3.height, count=1, crs=band3.crs, transform=band3.transform, dtype='float64')
                ndviImage.write(ndvi,1)
                ndviImage.close()
    elif str(sat_num) == '3':
        #pass landsat 3 logic
        band = row['product_band']
        if str(band) == 'SRB5':
            b5 = row['full_name']
            continue
        elif str(band) == 'SRB6':
            b6 = row['full_name']
            if b5[0:40] == b6[0:40]:
                print(b5)
                prefix = str(b5[0:40])
                print(b6)
                #ndvi calc
                print('ndvi calc')
                #import bands as separate 1 band raster
                band5 = rasterio.open(b5) #red
                band6 = rasterio.open(b6) #nir
                #generate nir and red objects as arrays in float64 format
                red = band5.read(1).astype('float64')
                nir = band6.read(1).astype('float64')
                #ndvi calculation, empty cells or nodata cells are reported as 0
                try:
                    ndvi=np.where((nir+red)==0., 0, (nir-red)/(nir+red))
                    ndvi[:5,:5]
                except:
                    print('Unable to process: '+ prefix)
                #export ndvi image
                ndviImage = rasterio.open(f_path+'/%s_ndvi.tif' % prefix,'w',driver='Gtiff', width=band5.width, height = band5.height, count=1, crs=band5.crs, transform=band5.transform, dtype='float64')
                ndviImage.write(ndvi,1)
                ndviImage.close() 
