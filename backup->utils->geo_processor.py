import geopandas as gpd
import json
from shapely.geometry import shape



# =====================================
# READ GEOJSON
# =====================================

def read_geojson(file):

    """
    Load GeoJSON boundary file
    """

    try:


        data = gpd.read_file(file)



        if data.empty:

            raise Exception(
                "GeoJSON contains no features"
            )



        # CRS check

        if data.crs is None:

            data = data.set_crs(
                epsg=4326
            )



        return data



    except Exception as e:


        raise Exception(

            f"GeoJSON Load Error: {e}"

        )





# =====================================
# AREA CALCULATION
# =====================================

def get_area(data):

    """
    Calculate area in square kilometer
    """

    try:


        # Convert WGS84 to meter projection

        projected = data.to_crs(
            epsg=3857
        )



        area = projected.area.sum()



        area_km = (

            area /

            1000000

        )



        return round(

            float(area_km),

            3

        )



    except Exception:


        return 0





# =====================================
# BOUNDARY LIMITS
# =====================================

def get_bounds(data):

    """
    Get GeoJSON bounding box
    """


    try:


        bounds = data.total_bounds



        return {


            "min_longitude":
            round(
                float(bounds[0]),
                6
            ),


            "min_latitude":
            round(
                float(bounds[1]),
                6
            ),


            "max_longitude":
            round(
                float(bounds[2]),
                6
            ),


            "max_latitude":
            round(
                float(bounds[3]),
                6
            )

        }



    except Exception:


        return {}





# =====================================
# CENTROID LOCATION
# =====================================

def get_centroid(data):

    """
    Find center point of boundary
    """


    try:


        centroid = data.geometry.centroid



        return {


            "latitude":

            round(

                float(
                    centroid.y.mean()
                ),

                6

            ),



            "longitude":

            round(

                float(
                    centroid.x.mean()
                ),

                6

            )

        }



    except Exception:


        return {}





# =====================================
# GEOMETRY INFORMATION
# =====================================

def get_geometry_info(data):

    """
    Extract geometry statistics
    """


    try:


        return {


            "features":

            len(data),



            "geometry_type":

            list(
                data.geometry.geom_type.unique()
            ),



            "crs":

            str(data.crs),



            "area_sq_km":

            get_area(data),



            "bounds":

            get_bounds(data),



            "centroid":

            get_centroid(data)

        }



    except Exception as e:


        return {


            "error":
            str(e)

        }





# =====================================
# CONVERT TO GEOJSON
# =====================================

def convert_to_geojson(data):

    """
    Convert GeoDataFrame
    into map compatible GeoJSON
    """


    try:


        return json.loads(

            data.to_json()

        )



    except Exception:


        return None





# =====================================
# POINT INSIDE BOUNDARY
# =====================================

def is_inside_boundary(
    data,
    latitude,
    longitude
):

    """
    Check if coordinate
    exists inside uploaded boundary
    """


    try:


        from shapely.geometry import Point



        point = Point(

            longitude,

            latitude

        )



        return bool(

            data.contains(point).any()

        )



    except Exception:


        return False
