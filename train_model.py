import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
)

import os
import json


# ==============================
# PATH
# ==============================

DATASET_PATH = "dataset"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "landcover_model.keras"
)

CLASS_PATH = os.path.join(
    MODEL_DIR,
    "classes.json"
)


HISTORY_PATH = os.path.join(
    MODEL_DIR,
    "history.json"
)


os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ==============================
# PARAMETERS
# ==============================

IMG_SIZE = 224

BATCH_SIZE = 16

EPOCHS = 15



# ==============================
# DATA AUGMENTATION
# ==============================


datagen = ImageDataGenerator(

    preprocessing_function=preprocess_input,

    validation_split=0.2,

    rotation_range=30,

    zoom_range=0.25,

    width_shift_range=0.15,

    height_shift_range=0.15,

    horizontal_flip=True,

    brightness_range=[0.8,1.2]

)



train_data = datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(IMG_SIZE,IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="training",

    shuffle=True

)



val_data = datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(IMG_SIZE,IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="validation",

    shuffle=False

)



# ==============================
# SAVE CLASSES
# ==============================


class_indices = train_data.class_indices


print("\nClasses:")
print(class_indices)


classes = list(class_indices.keys())


with open(CLASS_PATH,"w") as f:
    json.dump(classes,f,indent=4)



# ==============================
# MOBILE NET MODEL
# ==============================


base_model = MobileNetV2(

    weights="imagenet",

    include_top=False,

    input_shape=(
        IMG_SIZE,
        IMG_SIZE,
        3
    )

)


# Freeze pretrained layers

base_model.trainable = False



x = base_model.output


x = GlobalAveragePooling2D()(x)


x = Dropout(0.4)(x)


output = Dense(

    len(classes),

    activation="softmax"

)(x)



model = Model(

    inputs=base_model.input,

    outputs=output

)



# ==============================
# COMPILE
# ==============================


model.compile(

    optimizer=Adam(
        learning_rate=0.0001
    ),

    loss="categorical_crossentropy",

    metrics=[
        "accuracy"
    ]

)



model.summary()



# ==============================
# CALLBACKS
# ==============================


callbacks = [

    EarlyStopping(

        monitor="val_accuracy",

        patience=4,

        restore_best_weights=True

    ),


    ReduceLROnPlateau(

        monitor="val_loss",

        factor=0.3,

        patience=2,

        min_lr=1e-7

    ),


    ModelCheckpoint(

        MODEL_PATH,

        monitor="val_accuracy",

        save_best_only=True

    )

]



# ==============================
# TRAIN
# ==============================


history = model.fit(

    train_data,

    validation_data=val_data,

    epochs=EPOCHS,

    callbacks=callbacks

)



# ==============================
# SAVE HISTORY
# ==============================


with open(HISTORY_PATH,"w") as f:

    json.dump(

        history.history,

        f,

        indent=4

    )



print("\n==============================")
print("✅ TRAINING COMPLETE")
print("==============================")

print(
    "Model:",
    MODEL_PATH
)

print(
    "Classes:",
    CLASS_PATH
)

print(
    "History:",
    HISTORY_PATH
)
