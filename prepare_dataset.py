import os
import shutil
from pathlib import Path


# ==============================
# PATH
# ==============================

SOURCE = Path(
    "dataset/eurosat/EuroSAT_RGB"
)

DEST = Path(
    "dataset"
)


# ==============================
# CLASS MAPPING
# ==============================

mapping = {

    "Forest": "Forest",

    "AnnualCrop": "Agriculture",
    "PermanentCrop": "Agriculture",

    "River": "Water",
    "SeaLake": "Water",

    "Residential": "Urban",
    "Industrial": "Urban",
    "Highway": "Urban",

    "Pasture": "Barren",
    "HerbaceousVegetation": "Barren"

}



# ==============================
# COPY IMAGES
# ==============================

for source_class, target_class in mapping.items():


    source_folder = SOURCE / source_class

    target_folder = DEST / target_class


    target_folder.mkdir(
        exist_ok=True
    )


    if not source_folder.exists():

        print(
            "Missing:",
            source_folder
        )

        continue



    count = 0


    for image in source_folder.iterdir():


        if image.suffix.lower() in [
            ".jpg",
            ".jpeg",
            ".png"
        ]:


            shutil.copy(

                image,

                target_folder / image.name

            )


            count += 1



    print(
        source_class,
        "→",
        target_class,
        ":",
        count,
        "images"
    )



print(
    "\nDataset preparation completed"
)
