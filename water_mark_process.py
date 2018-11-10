#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
# from encodings import utf_8
from PIL import Image
from PIL import ImageChops

# from Auto_Watermark import DataBase


def main():

    water_mark_path = sys.argv[1]
    source_path = sys.argv[2]
    copy_path = os.path.join(os.getenv("TEMP"), "Auto_Water_Mark_Backup")
    # copy_path = DataBase.WATER_MARK_BACKUP
    print("Received and Processing: {0}".format(source_path))

    count = 0
    name = os.path.splitext(os.path.basename(source_path))[0]
    extension = os.path.splitext(os.path.basename(source_path))[1]

    while os.path.exists(
            os.path.join(copy_path, ("_".join((name, str(count)))) +
                         extension)):
        count += 1

    new_name = os.path.join(copy_path, ("_".join(
        (name, str(count)))) + extension)
    shutil.copy2(source_path, os.path.join(copy_path, new_name))

    try:
        image_file = Image.open(source_path)
        water_mark_file = Image.open(water_mark_path)

        comp_image = ImageChops.screen(image_file, water_mark_file)
        new_image = ImageChops.blend(image_file, comp_image, 0.3)

        new_image.save(source_path, format="JPEG", quality=100)

        image_file.close()
        water_mark_file.close()
        new_image.close()

    except FileNotFoundError:
        return


if __name__ == '__main__':

    main()
