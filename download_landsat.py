import ee
import geemap
import os

try:
    ee.Initialize(project='ee-alfanugraha')
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project='ee-alfanugraha')

asset_path =  'projects/ee-alfanugraha/assets/sumut_boundary' 
roi = ee.FeatureCollection(asset_path).geometry()

start = '2022-01-01'
end = '2023-04-30'

output_folder = r"D:\My_Code\02_Python\geepy\data"
output_filename = "landsat8_from_asset.tif"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
              .filterBounds(roi)
              .filterDate(start, end)
              .filter(ee.Filter.lt('CLOUD_COVER', 10)))

best_image = collection.sort('CLOUD_COVER').first()
scale_factor = 0.0000275
offset = -0.2
selected_bands = best_image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5'], ['Blue', 'Green', 'Red', 'NIR']) \
                           .multiply(scale_factor).add(offset)

final_image = selected_bands.clip(roi)

print(f"Using ROI from GEE Asset: {asset_path}")
print(f"Found image: {best_image.id().getInfo()}")
print("Downloading image as GeoTIFF...")

task = ee.batch.Export.image.toDrive(
    image=final_image,
    description='Landsat8_Export', # The name of the task in the GEE Tasks tab
    folder='sumut',                    # The folder name in your Google Drive
    fileNamePrefix=output_filename,
    scale=30,
    region=roi,
    fileFormat='GeoTIFF',
    maxPixels=1e13  # Increase maxPixels to handle large exports
)

# Start the task
task.start()

print("\n✅ Export task started successfully!")
print("➡️ Go to the GEE Code Editor 'Tasks' tab to monitor the export.")