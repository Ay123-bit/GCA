import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import json
import os
import sys

# ==============================
# PATHS
# ==============================

MODEL_PATH = "models/landcover_model.keras"
CLASS_PATH = "models/classes.json"

# ==============================
# LOAD MODEL
# ==============================

try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print("❌ Unable to load model.")
    print(e)
    exit()

# ==============================
# LOAD CLASSES
# ==============================

try:
    with open(CLASS_PATH, "r") as f:
        class_data = json.load(f)
except Exception as e:
    print("❌ Unable to load classes.json")
    print(e)
    exit()

if isinstance(class_data, list):
    classes = class_data

elif isinstance(class_data, dict):
    classes = [None] * len(class_data)
    for name, index in class_data.items():
        classes[index] = name

else:
    raise Exception("Invalid classes.json format")

# ==============================
# IMAGE PATH
# ==============================

if len(sys.argv) > 1:
    img_path = sys.argv[1]
else:
    img_path = "test.png"

if not os.path.exists(img_path):
    print("❌ Image not found!")
    print("Path:", img_path)
    exit()

ext = os.path.splitext(img_path)[1].lower()

if ext not in [".jpg", ".jpeg", ".png"]:
    print("❌ Unsupported image format.")
    exit()

# ==============================
# IMAGE PREPROCESSING
# ==============================

img = image.load_img(
    img_path,
    target_size=(224, 224)
)

img_array = image.img_to_array(img)

img_array = np.expand_dims(img_array, axis=0)

# IMPORTANT:
# Same preprocessing used by MobileNetV2
img_array = preprocess_input(img_array)

# ==============================
# PREDICTION
# ==============================

prediction = model.predict(img_array, verbose=0)[0]

best_index = np.argmax(prediction)
best_confidence = prediction[best_index]

# ==============================
# RESULT
# ==============================

print("\n==========================================")
print("        LAND COVER CLASSIFICATION")
print("==========================================")

print("Image       :", img_path)
print("Prediction  :", classes[best_index])
print("Confidence  : {:.2f}%".format(best_confidence * 100))

print("\nTop 3 Predictions")
print("------------------------------------------")

top3 = np.argsort(prediction)[::-1][:3]

for rank, idx in enumerate(top3, start=1):
    print(
        f"{rank}. {classes[idx]:15s} : {prediction[idx]*100:.2f}%"
    )

print("\nAll Class Probabilities")
print("------------------------------------------")

for cls, prob in zip(classes, prediction):
    print(f"{cls:15s} : {prob*100:.2f}%")

print("==========================================")
