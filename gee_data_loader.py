import ee
import numpy as np
import logging

logger = logging.getLogger(__name__)

def initialize_gee():
    ee.Initialize()
    logger.info("Google Earth Engine initialized successfully")

def get_sentinel2_data(lat, lon, start_date, end_date):
    # Define larger area of interest for accurate analysis
    point = ee.Geometry.Point([lon, lat])
    aoi = point.buffer(10000)  # 10km radius
    
    # Get best quality Sentinel-2 image
    collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                 .filterBounds(aoi)
                 .filterDate(start_date, end_date)
                 .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                 .sort('CLOUDY_PIXEL_PERCENTAGE')
                 .first())
    
    # Select bands and apply scaling
    red = collection.select('B4').multiply(0.0001)
    nir = collection.select('B8').multiply(0.0001)
    
    # Get higher resolution data
    scale = 20  # 20m resolution
    red_array = np.array(red.sampleRectangle(region=aoi, defaultValue=0).get('B4').getInfo())
    nir_array = np.array(nir.sampleRectangle(region=aoi, defaultValue=0).get('B8').getInfo())
    
    logger.info(f"Retrieved Sentinel-2 data: Red {red_array.shape}, NIR {nir_array.shape}")
    return red_array, nir_array