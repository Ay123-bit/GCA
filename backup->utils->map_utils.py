import folium



# ==============================
# CREATE INTERACTIVE MAP
# ==============================

def create_map(
        latitude,
        longitude,
        geojson_data=None,
        zoom_start=16
):

    """
    Create interactive GIS map

    Features:
    - Satellite location marker
    - GeoJSON boundary overlay
    - Layer control
    """



    # ==============================
    # BASE MAP
    # ==============================


    m = folium.Map(

        location=[

            latitude,

            longitude

        ],

        zoom_start=zoom_start,


        tiles=None

    )



    # ==============================
    # MAP LAYERS
    # ==============================


    folium.TileLayer(

        tiles="OpenStreetMap",

        name="Street Map",

        control=True

    ).add_to(m)



    folium.TileLayer(

        tiles=

        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",


        attr=

        "Esri Satellite",

        name="Satellite View",

        overlay=False,

        control=True

    ).add_to(m)



    # ==============================
    # LOCATION MARKER
    # ==============================


    folium.Marker(

        location=[

            latitude,

            longitude

        ],


        popup=folium.Popup(

            f"""

            <b>🛰️ Geo Compiler AI</b><br>

            Latitude: {latitude}<br>

            Longitude: {longitude}<br>

            Satellite Analysis Point

            """,

            max_width=300

        ),


        icon=folium.Icon(

            color="green",

            icon="leaf",

            prefix="fa"

        )


    ).add_to(m)




    # ==============================
    # GEOJSON BOUNDARY
    # ==============================


    if geojson_data is not None:



        folium.GeoJson(

            geojson_data,


            name="Analysis Boundary",


            style_function=lambda feature: {


                "fillColor":

                "#00ff00",


                "color":

                "green",


                "weight":

                3,


                "fillOpacity":

                0.25


            }


        ).add_to(m)



    # ==============================
    # MAP CONTROL
    # ==============================


    folium.LayerControl().add_to(m)



    return m
