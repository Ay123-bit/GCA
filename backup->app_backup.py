import streamlit as st
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import rasterio
import json
import time


from utils.image_analysis import analyze_image

from utils.ai_model import (
    predict_landcover,
    model_status
)

from utils.ndvi import (
    calculate_ndvi,
    analyze_ndvi,
    create_ndvi_map
)


from utils.raster_utils import (
    get_raster_location,
    calculate_real_ndvi
)


from utils.geo_processor import (
    read_geojson,
    get_area,
    convert_to_geojson,
    get_geometry_info
)


from utils.map_utils import create_map


from streamlit_folium import st_folium




# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Geo Compiler AI",

    page_icon="🛰️",

    layout="wide"

)



# =====================================
# HEADER
# =====================================

st.title(
    "🛰️ Geo Compiler AI"
)


st.subheader(
    "Deep Learning Satellite Image Intelligence System"
)


st.write(
    "CNN Based Land Cover Classification + NDVI + GIS Analysis"
)



st.divider()



# =====================================
# MODEL STATUS
# =====================================


status = model_status()



if status["status"] == "Loaded":


    st.success(

        "🧠 CNN Land Cover AI Model Active"

    )


else:


    st.error(

        "❌ CNN Model Not Loaded"

    )



st.divider()





# =====================================
# VARIABLES
# =====================================


if "analysis_done" not in st.session_state:

    st.session_state.analysis_done = False



raster_info = {}

geojson_data = None

area = 0

latitude = 20.296100

longitude = 85.824500






# =====================================
# IMAGE UPLOAD
# =====================================


uploaded_file = st.file_uploader(

    "Upload Satellite Image",

    type=[

        "jpg",
        "jpeg",
        "png",
        "tif",
        "tiff"

    ]

)





if uploaded_file:



    file_name = uploaded_file.name.lower()




    # =====================================
    # GEOTIFF METADATA
    # =====================================


    if file_name.endswith(

        (".tif",".tiff")

    ):


        try:


            uploaded_file.seek(0)



            raster_info = get_raster_location(

                uploaded_file

            )



            if "error" not in raster_info:


                latitude = raster_info["latitude"]

                longitude = raster_info["longitude"]



                st.success(

                    "🛰️ GeoTIFF Metadata Loaded"

                )



                with st.expander(

                    "📍 Raster Information"

                ):


                    st.json(

                        raster_info

                    )



        except Exception as e:


            st.warning(

                f"Raster metadata error : {e}"

            )






    # =====================================
    # IMAGE READING
    # =====================================


    try:



        if file_name.endswith(

            (".tif",".tiff")

        ):



            uploaded_file.seek(0)



            with rasterio.open(

                uploaded_file

            ) as src:



                if src.count >= 3:



                    img_rgb = src.read(

                        [3,2,1]

                    )



                    img_rgb = np.moveaxis(

                        img_rgb,

                        0,

                        -1

                    )


                else:


                    img_rgb = src.read(1)





        else:



            uploaded_file.seek(0)


            img_rgb = np.array(

                Image.open(

                    uploaded_file

                )

            )





        # normalize satellite data


        if img_rgb.dtype != np.uint8:


            img_rgb = cv2.normalize(

                img_rgb,

                None,

                0,

                255,

                cv2.NORM_MINMAX

            ).astype(

                np.uint8

            )





    except Exception as e:


        st.error(

            f"Image Loading Failed : {e}"

        )


        st.stop()





    # =====================================
    # COLOR CONVERSION
    # =====================================


    if len(img_rgb.shape)==2:



        img = cv2.cvtColor(

            img_rgb,

            cv2.COLOR_GRAY2BGR

        )



        display_img = cv2.cvtColor(

            img_rgb,

            cv2.COLOR_GRAY2RGB

        )



    else:



        img = cv2.cvtColor(

            img_rgb,

            cv2.COLOR_RGB2BGR

        )


        display_img = img_rgb






    # =====================================
    # AI ANALYSIS
    # =====================================


    with st.spinner(

        "🧠 Running CNN Satellite AI..."

    ):



        start = time.time()



        image_result = analyze_image(

            img

        )



        ai_result = predict_landcover(

            img

        )



        ndvi = calculate_ndvi(

            img

        )



        inference_time = time.time()-start




    st.success(

        f"AI Analysis Completed ({inference_time:.2f}s)"

    )





    # =====================================
    # REAL NDVI
    # =====================================


    if file_name.endswith(

        (".tif",".tiff")

    ):



        uploaded_file.seek(0)



        real_ndvi = calculate_real_ndvi(

            uploaded_file

        )


        if real_ndvi is not None:


            ndvi = real_ndvi


            st.success(

                "🌱 Real Satellite NDVI Generated"

            )
                # =====================================
    # AI METRICS
    # =====================================


    st.divider()

    st.subheader(
        "🤖 Deep Learning AI Results"
    )


    col1,col2,col3,col4 = st.columns(4)



    with col1:

        st.metric(

            "Land Cover",

            ai_result.get(

                "class",

                "Unknown"

            )

        )



    with col2:

        confidence = ai_result.get(

            "confidence",

            0

        )


        st.metric(

            "Confidence",

            f"{confidence*100:.2f}%"

        )



    with col3:

        st.metric(

            "Inference Time",

            f"{inference_time:.2f}s"

        )



    with col4:

        st.metric(

            "NDVI",

            round(

                float(np.mean(ndvi)),

                3

            )

        )





    # =====================================
    # AI JSON DETAILS
    # =====================================


    with st.expander(

        "View AI Prediction Details"

    ):


        st.json(

            ai_result

        )






    st.divider()





    # =====================================
    # IMAGE DISPLAY
    # =====================================


    st.subheader(

        "🛰️ Satellite Image"

    )



    st.image(

        display_img,

        caption="Input Satellite Image",

        use_container_width=True

    )







    # =====================================
    # FEATURE DETECTION
    # =====================================


    st.subheader(

        "🔍 Feature Detection"

    )


    edges = image_result.get(

        "edges",

        None

    )



    if edges is not None:



        if len(edges.shape)==2:



            edges_display = cv2.cvtColor(

                edges,

                cv2.COLOR_GRAY2RGB

            )


        else:


            edges_display = edges





        st.image(

            edges_display,

            caption="Detected Features",

            use_container_width=True

        )



    else:


        st.info(

            "Feature detection unavailable"

        )







    # =====================================
    # NDVI ANALYSIS
    # =====================================


    st.divider()


    st.subheader(

        "🌱 NDVI Vegetation Analysis"

    )



    ndvi = np.nan_to_num(

        ndvi

    )



    ndvi_score = float(

        np.mean(ndvi)

    )



    st.write(

        "Average NDVI:",

        round(

            ndvi_score,

            3

        )

    )





    # NDVI health


    ndvi_report = analyze_ndvi(

        ndvi

    )



    c1,c2,c3 = st.columns(3)



    with c1:


        st.metric(

            "Healthy Vegetation",

            f"{ndvi_report['healthy_percentage']}%"

        )



    with c2:


        st.metric(

            "Moderate Vegetation",

            f"{ndvi_report['moderate_percentage']}%"

        )



    with c3:


        st.metric(

            "Poor Vegetation",

            f"{ndvi_report['poor_percentage']}%"

        )







    # NDVI MAP


    ndvi_image = create_ndvi_map(

        ndvi

    )



    st.image(

        ndvi_image,

        caption="NDVI Heat Map",

        use_container_width=True

    )





    st.divider()






    # =====================================
    # GEOJSON ANALYSIS
    # =====================================


    st.subheader(

        "📂 GeoJSON Boundary Analysis"

    )



    geo_file = st.file_uploader(

        "Upload GeoJSON Boundary",

        type=[

            "geojson",

            "json"

        ]

    )





    if geo_file:



        try:



            geo = read_geojson(

                geo_file

            )



            area = get_area(

                geo

            )



            geojson_data = convert_to_geojson(

                geo

            )



            geometry_info = get_geometry_info(

                geo

            )



            st.success(

                "GeoJSON Loaded Successfully"

            )



            st.metric(

                "Boundary Area",

                f"{area} sq km"

            )



            with st.expander(

                "Boundary Details"

            ):



                st.json(

                    geometry_info

                )



        except Exception as e:



            st.error(

                f"GeoJSON Error : {e}"

            )







    st.divider()





    # =====================================
    # MAP SECTION
    # =====================================


    st.subheader(

        "🗺️ Geospatial Map"

    )



    latitude = st.number_input(

        "Latitude",

        value=float(latitude),

        format="%.6f"

    )



    longitude = st.number_input(

        "Longitude",

        value=float(longitude),

        format="%.6f"

    )





    try:



        map_obj = create_map(

            latitude,

            longitude,

            geojson_data

        )



        st_folium(

            map_obj,

            width=900,

            height=600

        )



    except Exception as e:



        st.error(

            f"Map Error : {e}"

        )
            # =====================================
    # AI REPORT GENERATION
    # =====================================


    st.divider()


    st.subheader(

        "📄 AI Report Generation"

    )



    report_data = {


        "generated_time":

        str(datetime.now()),



        "image_name":

        uploaded_file.name,



        "ai_model":

        "CNN Deep Learning Land Cover Model",



        "land_cover":

        ai_result.get(

            "class",

            "Unknown"

        ),



        "confidence":

        round(

            ai_result.get(

                "confidence",

                0

            ) * 100,

            2

        ),



        "class_id":

        ai_result.get(

            "class_id",

            None

        ),



        "terrain_classification":

        image_result.get(

            "category",

            "Unknown"

        ),



        "brightness":

        image_result.get(

            "brightness",

            0

        ),



        "vegetation_index":

        image_result.get(

            "vegetation_index",

            0

        ),



        "average_ndvi":

        round(

            ndvi_score,

            3

        ),



        "ndvi_analysis":

        ndvi_report,



        "boundary_area_sq_km":

        area,



        "latitude":

        latitude,



        "longitude":

        longitude,



        "raster_information":

        raster_info



    }





    # =====================================
    # JSON REPORT
    # =====================================


    json_report = json.dumps(

        report_data,

        indent=4

    )



    st.download_button(


        label="⬇️ Download JSON AI Report",


        data=json_report,


        file_name=

        "GeoCompilerAI_Report.json",


        mime=

        "application/json"


    )







    # =====================================
    # TEXT REPORT
    # =====================================


    text_report = f"""

=====================================
        GEO COMPILER AI REPORT
=====================================


Generated Time:

{datetime.now()}



Image:

{uploaded_file.name}



AI MODEL:

CNN Deep Learning Model



LAND COVER:

{ai_result.get("class","Unknown")}



CONFIDENCE:

{ai_result.get("confidence",0)*100:.2f}%



CLASS ID:

{ai_result.get("class_id","NA")}



TERRAIN:

{image_result.get("category","Unknown")}



BRIGHTNESS:

{image_result.get("brightness",0)}



VEGETATION INDEX:

{image_result.get("vegetation_index",0)}



AVERAGE NDVI:

{round(ndvi_score,3)}



NDVI HEALTH:

Healthy:

{ndvi_report.get("healthy_percentage",0)}%


Moderate:

{ndvi_report.get("moderate_percentage",0)}%


Poor:

{ndvi_report.get("poor_percentage",0)}%



BOUNDARY AREA:

{area} sq km



LOCATION:

Latitude:
{latitude}


Longitude:
{longitude}



RASTER CRS:

{raster_info.get("crs","NA")}



BANDS:

{raster_info.get("bands","NA")}



RESOLUTION:

{raster_info.get("resolution_x","NA")}

x

{raster_info.get("resolution_y","NA")}



Generated By:

Geo Compiler AI


=====================================

"""





    st.download_button(


        label="⬇️ Download TXT Report",


        data=text_report,


        file_name=

        "GeoCompilerAI_Report.txt",


        mime=

        "text/plain"


    )






    # =====================================
    # FINAL STATUS
    # =====================================


    st.success(

        "✅ Complete Satellite Analysis Finished"

    )





# =====================================
# NO FILE UPLOADED
# =====================================


else:



    st.info(

        "🛰️ Upload satellite image to start CNN based analysis"

    )
