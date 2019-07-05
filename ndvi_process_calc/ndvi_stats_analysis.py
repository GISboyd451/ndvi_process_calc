
import os 
import sys
import pandas as pd 
import rasterio
import numpy as np
from glob import glob



f_path = 'T:/ProjectsNational/NationalDataQuality/Sprint/Alec_scripts/tia_ndvi/scenes/analysis_ready/combined_test'

# Combined test:
# Test to see if we can just throw everything into one location and then process.
try:
    os.chdir('T:/ProjectsNational/NationalDataQuality/Sprint/Alec_scripts/tia_ndvi/scenes/analysis_ready/combined_test')
    print("Folder found.")
except:
    print("Folder not found.")

try:
    user_database = pd.read_csv("user_database.csv")
    print('csv found.')
except:
    print('csv not found.')

#print(user_database.head())

# Get list of ndvi files by pattern
file_list = glob(os.path.join('*ndvi.tif'))

# Parse out the file names by character stripping, to get the satellite information from the NDVI file name.
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
ndvi_database = pd.DataFrame(
    {'satellite':satellite,
    'processing':processing,
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
ndvi_database["full_date"] = ndvi_database["year"].map(str) + ndvi_database["month"].map(str) + ndvi_database["day"].map(str)

# Reorder database table
ndvi_database = ndvi_database.sort_values(by=['full_date', 'product_band'])
#print(ndvi_database.head())

# Append ndvi raster metadata to a txt file for future reference. If ndvi text file exists, skip this step as we do not want to duplicate metadata. If new data is needed here,
# simply delete then txt file and the script will rerun this section.

if not os.path.exists("ndvi_meta.txt"):
    for i, row in ndvi_database.iterrows():
        raster = rasterio.open(row['full_name'])
        with open("ndvi_meta.txt", "a") as myfile:
            myfile.write(row['full_name'])
            myfile.write("\n")
            myfile.write(str(raster.meta))
            myfile.write("\n")
            myfile.write("\n")
else:
    print("ndvi metadata txt file already exists, skipping txt file creation.")
#

# Get ndvi band statistics
stats = []
for i, row in ndvi_database.iterrows():
    print(row['full_name'])
    raster = rasterio.open(row['full_name'])
    array = raster.read()
    stats.append({
        'min': array.min(),
        'mean': array.mean(),
        'median': np.median(array),
        'max': array.max(),
        'std': np.std(array)
    })

stats = pd.DataFrame(stats)
#print(stats)
ndvi_database = pd.merge(ndvi_database, stats, how='left', left_index=True,right_index=True)
#print(ndvi_database.head())

