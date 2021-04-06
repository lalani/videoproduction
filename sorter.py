import math
import os
from os import listdir
from os.path import isfile, join, splitext
from pathlib import Path
from shutil import copyfile

import cv2
import numpy as np


def get_image_orientation(file_name):
    filename, file_extension = splitext(file_name)
    if file_extension.lower()[1:] not in ["jpg", "png", "jpeg", "tif", "tiff"]:
        print(f"unsupported file {file_extension}")
        return None
    img = cv2.imread(file_name)
    y, x, _ = img.shape
    if x > y:
        return "landscape"
    else:
        return "portrait"


if __name__ == '__main__':
    num_img_per_bucket = 50
    main_dir = "D:/Design/COL/media"
    directories = ["ECD Highlights", "ECD Highlights - Central", "ECD Highlights - Florida", "ECD Highlights - Midwest",
                   "ECD Highlights - Northeast", "ECD Highlights - Southeast", "ECD Highlights - Southwest"]

    # dir_counter = 0
    all_images = []
    for my_dir in directories:
        mypath = f"{main_dir}/{my_dir}"
        onlyfiles = [f"{main_dir}/{my_dir}/{f}" for f in listdir(mypath) if isfile(join(mypath, f))]
        all_images.extend(onlyfiles)

    np.random.shuffle(all_images)
    landscape_images_only = []
    portrait_images_only = []
    for image in all_images:
        img_orientation = get_image_orientation(image)
        if img_orientation == "landscape":
            landscape_images_only.append(image)
        elif img_orientation == "portrait":
            portrait_images_only.append(image)

    print(f"num of images: {len(landscape_images_only)}")

    # purposely floors, so not all images are used
    target_buckets = math.floor(len(landscape_images_only) / num_img_per_bucket)
    buckets = []
    start_index = 0
    img_id = 0
    for i in range(target_buckets):
        image_set = landscape_images_only[start_index:start_index + num_img_per_bucket]
        output_dir = f"{main_dir}/output/landscape{i}"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_file_list = f"{main_dir}/output/landscape{i}.txt"
        with open(output_file_list, 'w') as f:
            for line in image_set:
                f.write(f"{line}\n")

        for img_name_orig in image_set:
            filename, file_extension = splitext(img_name_orig)
            img_name_new = f"{output_dir}/image{img_id}{file_extension}"
            copyfile(img_name_orig, img_name_new)
            img_id += 1

        start_index += num_img_per_bucket

    output_dir = f"{main_dir}/output/landscape_leftovers"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_file_list = f"{main_dir}/output/landscape_leftovers.txt"
    left_over_images = landscape_images_only[start_index:]
    with open(output_file_list, 'w') as f:
        for line in left_over_images:
            f.write(f"{line}\n")
    for img_name_orig in left_over_images:
        filename, file_extension = splitext(img_name_orig)
        img_name_new = f"{output_dir}/image{img_id}{file_extension}"
        copyfile(img_name_orig, img_name_new)
        img_id += 1

    output_dir = f"{main_dir}/output/portraits"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_file_list = f"{main_dir}/output/portraits.txt"
    with open(output_file_list, 'w') as f:
        for line in portrait_images_only:
            f.write(f"{line}\n")

    img_id = 0
    for img_name_orig in portrait_images_only:
        filename, file_extension = splitext(img_name_orig)
        img_name_new = f"{output_dir}/image{img_id}{file_extension}"
        copyfile(img_name_orig, img_name_new)
        img_id += 1
