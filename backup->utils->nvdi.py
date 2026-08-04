import numpy as np
import cv2




# ==============================
# RGB NDVI CALCULATION
# ==============================

def calculate_ndvi(image):

    """
    Approximate NDVI for RGB images.

    Formula:

    (Green - Red) / (Green + Red)

    For satellite GeoTIFF:
    use calculate_real_ndvi()
    from raster_utils.py
    """


    try:


        image = image.astype(

            np.float32

        )



        red = image[:,:,0]

        green = image[:,:,1]



        numerator = (

            green - red

        )


        denominator = (

            green + red + 0.0001

        )



        ndvi = numerator / denominator



        ndvi = np.clip(

            ndvi,

            -1,

            1

        )



        return ndvi




    except Exception as e:


        print(
            "NDVI Error:",
            e
        )


        return np.zeros(

            (

                image.shape[0],

                image.shape[1]

            ),

            dtype=np.float32

        )






# ==============================
# REAL SATELLITE NDVI
# ==============================

def calculate_band_ndvi(red_band, nir_band):

    """
    Real satellite NDVI

    Sentinel-2:
    Red = Band 4
    NIR = Band 8


    Landsat:
    Red = Band 4
    NIR = Band 5
    """



    try:


        red = red_band.astype(

            np.float32

        )


        nir = nir_band.astype(

            np.float32

        )



        ndvi = (

            nir - red

        ) / (

            nir + red + 0.0001

        )



        ndvi = np.clip(

            ndvi,

            -1,

            1

        )


        return ndvi



    except Exception as e:


        print(

            "Band NDVI Error:",

            e

        )


        return None






# ==============================
# NDVI HEALTH ANALYSIS
# ==============================

def analyze_ndvi(ndvi):

    """
    Vegetation health classification
    """


    ndvi = np.nan_to_num(

        ndvi

    )


    total = ndvi.size



    if total == 0:


        return {}



    healthy = np.sum(

        ndvi >= 0.6

    )



    moderate = np.sum(

        (

            ndvi >= 0.3

        )

        &

        (

            ndvi < 0.6

        )

    )



    low = np.sum(

        (

            ndvi >= 0

        )

        &

        (

            ndvi < 0.3

        )

    )



    barren = np.sum(

        ndvi < 0

    )




    return {


        "average_ndvi":

        round(

            float(

                np.mean(ndvi)

            ),

            3

        ),



        "healthy vegetation %":

        round(

            healthy / total * 100,

            2

        ),



        "moderate vegetation %":

        round(

            moderate / total * 100,

            2

        ),



        "low vegetation %":

        round(

            low / total * 100,

            2

        ),



        "water_or_barren %":

        round(

            barren / total * 100,

            2

        )

    }






# ==============================
# NDVI CATEGORY
# ==============================

def ndvi_category(value):

    """
    Convert NDVI value into class
    """


    if value < 0:


        return "Water / No Vegetation 💧"



    elif value < 0.3:


        return "Poor Vegetation 🟤"



    elif value < 0.6:


        return "Healthy Vegetation 🌱"



    else:


        return "Dense Vegetation 🌳"







# ==============================
# NDVI HEATMAP
# ==============================

def create_ndvi_map(ndvi):

    """
    Create NDVI visualization map
    """


    ndvi = np.nan_to_num(

        ndvi

    )



    normalized = cv2.normalize(

        ndvi,

        None,

        0,

        255,

        cv2.NORM_MINMAX

    ).astype(

        np.uint8

    )



    heatmap = cv2.applyColorMap(

        normalized,

        cv2.COLORMAP_TURBO

    )



    rgb_heatmap = cv2.cvtColor(

        heatmap,

        cv2.COLOR_BGR2RGB

    )



    return rgb_heatmap
