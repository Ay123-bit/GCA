import cv2
import numpy as np
import tensorflow as tf
import os


CLASSES = [
    "Forest 🌳",
    "Agriculture 🌱",
    "Water 💧",
    "Urban 🏙️",
    "Barren Land 🏜️"
]


MODEL_PATH = "models/landcover_model.h5"


model = None



def load_model():

    global model

    try:

        if os.path.exists(MODEL_PATH):

            model = tf.keras.models.load_model(
                MODEL_PATH
            )

            print("✅ CNN Land Cover Model Loaded")

        else:

            print(
                "❌ Model file not found:",
                MODEL_PATH
            )


    except Exception as e:

        print(
            "Model Load Error:",
            e
        )



load_model()




def preprocess_image(image):

    img = cv2.resize(
        image,
        (224,224)
    )


    img = img.astype(
        "float32"
    )


    img = img / 255.0


    img = np.expand_dims(
        img,
        axis=0
    )


    return img




def predict_landcover(image):

    """
    Deep Learning Land Cover Classification
    No Rule Based Logic
    """

    try:


        if model is None:

            return {

                "class":
                "AI Model Not Loaded",

                "confidence":
                0

            }



        processed = preprocess_image(
            image
        )



        prediction = model.predict(
            processed,
            verbose=0
        )



        class_id = int(
            np.argmax(
                prediction[0]
            )
        )



        confidence = float(
            np.max(
                prediction[0]
            )
        )



        return {


            "class":
            CLASSES[class_id],


            "confidence":
            round(
                confidence,
                4
            ),


            "class_id":
            class_id

        }



    except Exception as e:


        return {

            "class":
            "Prediction Error",

            "confidence":
            0,

            "error":
            str(e)

        }




def model_status():

    if model is None:

        return {

            "status":
            "Not Loaded"

        }


    return {

        "status":
        "Loaded",

        "classes":
        len(CLASSES)

    }
