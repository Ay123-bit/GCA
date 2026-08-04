import cv2
import numpy as np


def analyze_image(img):

    result = {}

    try:

        # ==============================
        # IMAGE VALIDATION
        # ==============================

        if img is None:
            raise Exception("Image not found")


        # ==============================
        # GRAY IMAGE
        # ==============================

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )


        # ==============================
        # BRIGHTNESS
        # ==============================

        brightness = float(
            np.mean(gray)
        )


        # ==============================
        # VEGETATION DETECTION
        # ==============================

        hsv = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2HSV
        )


        green_mask = cv2.inRange(
            hsv,
            np.array([35,40,40]),
            np.array([85,255,255])
        )


        vegetation_pixels = np.sum(
            green_mask > 0
        )


        total_pixels = green_mask.size


        vegetation_index = (
            vegetation_pixels /
            total_pixels
        ) * 100



        # ==============================
        # FEATURE / EDGE DETECTION
        # ==============================

        blur = cv2.GaussianBlur(
            gray,
            (5,5),
            0
        )


        edges = cv2.Canny(
            blur,
            20,
            80
        )


        # Remove noise

        kernel = np.ones(
            (3,3),
            np.uint8
        )


        edges = cv2.dilate(
            edges,
            kernel,
            iterations=1
        )


        edges = cv2.convertScaleAbs(
            edges
        )


        # Convert edge image to RGB
        # for Streamlit display

        edges_display = cv2.cvtColor(
            edges,
            cv2.COLOR_GRAY2RGB
        )



        # ==============================
        # TERRAIN CLASSIFICATION
        # ==============================

        if vegetation_index >= 50:

            category = "Dense Vegetation 🌳"


        elif vegetation_index >= 20:

            category = "Vegetation Area 🌱"


        elif brightness > 180:

            category = "Dry/Barren Land 🏜️"


        elif brightness < 60:

            category = "Water/Dark Area 🌊"


        else:

            category = "Mixed Terrain"



        # ==============================
        # RESULT
        # ==============================

        result = {

            "category": category,


            "brightness": round(
                brightness,
                2
            ),


            "vegetation_index": round(
                vegetation_index,
                2
            ),


            "edges": edges_display,


            "green_mask": green_mask

        }



    except Exception as e:


        result = {

            "category": "Unknown",

            "brightness": 0,

            "vegetation_index": 0,

            "edges": None,

            "error": str(e)

        }



    return result
