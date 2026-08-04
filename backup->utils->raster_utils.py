import numpy as np
import rasterio
from rasterio.warp import transform_bounds


# =====================================
# GET RASTER METADATA + LOCATION
# =====================================

def get_raster_location(file):

    """
    Extract GeoTIFF metadata,
    CRS and GPS coordinates.
    """

    try:

        with rasterio.open(file) as src:


            bounds = src.bounds

            crs = src.crs



            if crs is None:

                raise Exception(
                    "CRS information not available"
                )



            # Convert projection to GPS

            west, south, east, north = transform_bounds(

                crs,

                "EPSG:4326",

                bounds.left,

                bounds.bottom,

                bounds.right,

                bounds.top

            )



            latitude = (

                south + north

            ) / 2



            longitude = (

                west + east

            ) / 2



            return {


                "latitude":
                float(latitude),


                "longitude":
                float(longitude),


                "west":
                float(west),


                "south":
                float(south),


                "east":
                float(east),


                "north":
                float(north),



                "crs":
                str(crs),



                "bands":
                src.count,



                "width":
                src.width,


                "height":
                src.height,



                "resolution_x":
                float(src.res[0]),



                "resolution_y":
                float(src.res[1]),



                "driver":
                src.driver

            }



    except Exception as e:


        return {


            "error":
            str(e)

        }





# =====================================
# REAL SATELLITE NDVI
# =====================================


def calculate_real_ndvi(file):

    """
    Calculate real NDVI from GeoTIFF.

    Sentinel-2:
        Red = Band 4
        NIR = Band 8

    Landsat:
        Red = Band 4
        NIR = Band 5

    Returns:
        NDVI numpy array
    """



    try:


        with rasterio.open(file) as src:


            band_count = src.count



            # -------------------------
            # Sentinel-2
            # -------------------------

            if band_count >= 8:


                red = src.read(
                    4
                ).astype(
                    np.float32
                )


                nir = src.read(
                    8
                ).astype(
                    np.float32
                )



            # -------------------------
            # Landsat
            # -------------------------

            elif band_count >= 5:


                red = src.read(
                    4
                ).astype(
                    np.float32
                )


                nir = src.read(
                    5
                ).astype(
                    np.float32
                )



            else:


                raise Exception(

                    "GeoTIFF does not contain required Red and NIR bands"

                )



            # -------------------------
            # Handle NoData
            # -------------------------

            red[red == src.nodata] = np.nan

            nir[nir == src.nodata] = np.nan



            # -------------------------
            # NDVI Formula
            # -------------------------

            denominator = (

                nir + red + 0.0001

            )



            ndvi = (

                nir - red

            ) / denominator



            # Remove invalid values

            ndvi = np.nan_to_num(

                ndvi,

                nan=0.0,

                posinf=0.0,

                neginf=0.0

            )



            # NDVI range

            ndvi = np.clip(

                ndvi,

                -1,

                1

            )



            return ndvi





    except Exception as e:


        print(

            "Real NDVI Error:",

            e

        )


        return None





# =====================================
# NDVI STATISTICS
# =====================================


def ndvi_statistics(ndvi):

    """
    Generate vegetation statistics.
    """


    if ndvi is None:

        return {

            "average":0,

            "vegetation":0

        }



    ndvi = np.nan_to_num(
        ndvi
    )



    vegetation = np.sum(

        ndvi > 0.3

    )



    total = ndvi.size



    return {


        "average":round(

            float(
                np.mean(ndvi)
            ),

            3

        ),



        "vegetation_percentage":round(

            (
                vegetation /
                total
            ) * 100,

            2

        )

    }
