# ============================================================
# GEO COMPILER AI
# Advanced Satellite GIS Layer Engine V2
# utils/satellite_layers.py
# ============================================================


import folium

from folium.raster_layers import TileLayer, ImageOverlay




# ============================================================
# TILE CONSTANTS
# ============================================================


ESRI_SATELLITE = (

    "https://server.arcgisonline.com/"
    "ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"

)



ESRI_HYBRID = (

    "https://services.arcgisonline.com/"
    "ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"

)



ESRI_LABELS = (

    "https://services.arcgisonline.com/"
    "ArcGIS/rest/services/"
    "Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"

)



OPEN_STREET = (

    "https://tile.openstreetmap.org/"
    "{z}/{x}/{y}.png"

)



TERRAIN = (

    "https://tile.opentopomap.org/"
    "{z}/{x}/{y}.png"

)




CARTO_DARK = (

    "https://{s}.basemaps.cartocdn.com/"
    "dark_all/{z}/{x}/{y}{r}.png"

)





# ============================================================
# CREATE SATELLITE LAYERS
# ============================================================


def create_satellite_layers(

        latitude=None,

        longitude=None

):

    """
    Returns Folium GIS layers

    """

    try:


        layers=[]



        # Satellite


        layers.append(

            TileLayer(

                tiles=ESRI_SATELLITE,

                attr="Esri World Imagery",

                name="🛰️ Satellite Imagery",

                overlay=False,

                control=True

            )

        )




        # Open Street


        layers.append(

            TileLayer(

                tiles=OPEN_STREET,

                attr="OpenStreetMap",

                name="🗺️ Street Map",

                overlay=False,

                control=True

            )

        )





        # Terrain


        layers.append(

            TileLayer(

                tiles=TERRAIN,

                attr="OpenTopoMap",

                name="⛰️ Terrain",

                overlay=False,

                control=True

            )

        )






        # Dark Map


        layers.append(

            TileLayer(

                tiles=CARTO_DARK,

                attr="CartoDB",

                name="🌑 Dark GIS",

                overlay=False,

                control=True

            )

        )






        # Hybrid Satellite


        layers.append(

            TileLayer(

                tiles=ESRI_HYBRID,

                attr="Esri Hybrid",

                name="🌍 Hybrid Satellite",

                overlay=True,

                control=True

            )

        )




        # Labels


        layers.append(

            TileLayer(

                tiles=ESRI_LABELS,

                attr="Esri Labels",

                name="🏷️ Map Labels",

                overlay=True,

                control=True

            )

        )




        return layers




    except Exception as e:


        print(

            "Satellite Layer Error:",

            e

        )


        return []







# ============================================================
# ADD LAYERS
# ============================================================


def add_satellite_layers(

        map_object,

        layers

):


    try:


        if not layers:

            return map_object



        for layer in layers:


            layer.add_to(

                map_object

            )



        return map_object



    except Exception as e:


        print(

            "Layer Add Error:",

            e

        )


        return map_object







# ============================================================
# NDVI IMAGE OVERLAY
# ============================================================


def create_ndvi_overlay(

        image,

        bounds=None,

        name="🌱 NDVI Layer"

):


    try:


        overlay = ImageOverlay(

            image=image,

            bounds=bounds,

            opacity=0.65,

            name=name,

            interactive=True,

            cross_origin=False

        )



        return overlay



    except Exception as e:


        print(

            "NDVI Overlay Error:",

            e

        )


        return None







# ============================================================
# GEOJSON BOUNDARY
# ============================================================


def add_boundary_layer(

        map_object,

        geojson,

        name="📍 Analysis Boundary"

):


    try:


        boundary = folium.GeoJson(


            geojson,


            name=name,


            style_function=lambda x:{


                "color":"#00ff88",

                "weight":3,

                "fillColor":"#00ff88",

                "fillOpacity":0.25

            }


        )



        boundary.add_to(

            map_object

        )



        return boundary



    except Exception as e:


        print(

            "Boundary Error:",

            e

        )


        return None







# ============================================================
# COMPLETE GIS PIPELINE
# ============================================================


def setup_gis_layers(

        map_object,

        geojson=None,

        ndvi_image=None,

        ndvi_bounds=None

):


    try:



        layers=create_satellite_layers()



        add_satellite_layers(

            map_object,

            layers

        )




        if geojson:


            add_boundary_layer(

                map_object,

                geojson

            )





        if ndvi_image is not None:


            overlay=create_ndvi_overlay(

                ndvi_image,

                ndvi_bounds

            )


            if overlay:


                overlay.add_to(

                    map_object

                )





        folium.LayerControl(

            collapsed=False

        ).add_to(

            map_object

        )



        return map_object




    except Exception as e:


        print(

            "GIS Pipeline Error:",

            e

        )


        return map_object
