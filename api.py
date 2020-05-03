# -*- coding=utf8 -*-
import os
import sys
import cv2
import logging
import datetime

from lib.config import cfg_from_file, cfg
from lib.detector import detect as plate_detect
from lib.recognizer import recognize as chars_recognize
from lib.utils.align import align

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # display chinese title in plt
plt.rcParams['axes.unicode_minus'] = False  # display minus normally

logging.basicConfig(level=logging.INFO)

class PlateAPI(object):
    def __init__(self, cfg_filepath=".\\cfgs\\easypr.yml"):
        cfg_from_file(cfg_filepath)
        self._cfg = cfg

    def __detect(self, image_filepath):
        """
        Supposed to be called internally
        """
        if not os.path.isfile(image_filepath):
            logging.error(
                "PlateAPI.Detect: ImagePath[%s] was not a valid file" % image_filepath)
            return None
        image = cv2.imread(image_filepath)
        seg_images = plate_detect(image)
        res = []
        for x in seg_images:
            res.append(align(image, x))
        return res, image

    def __recognize(self, image):
        """
        Recognize single extracted plate image
        """
        plate_char = chars_recognize(image)
        logging.info(plate_char)
        logging.info("Chars Recognize: %s" % str(plate_char))
        return plate_char

    def __save(self, original_image, plate_image_list, plate_char_list):
        current_ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        base_path = str(self._cfg.SAVE_PATH) + "\\%s" % current_ts
        print(base_path)
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        logging.info("PlateAPI.Save: saving files to [%s]" % (base_path))
        cv2.imwrite(str(self._cfg.SAVE_PATH_ORIGINAL_IMG) % current_ts, original_image)
        for single_plate, plate_char in zip(plate_image_list, plate_char_list):
            logging.info("Saving plate[%s] to path[%s]" % (
                str(plate_char), str(self._cfg.SAVE_PATH_PLATE_SEG) % (current_ts, str(plate_char))))
            cv2.imwrite(str(self._cfg.SAVE_PATH_PLATE_SEG) %
                        (current_ts, str(plate_char)), single_plate)

    def process(self, image_filepath):
        """
        Process both detection and recognition
        """
        images, original_image = self.__detect(image_filepath)
        char_list = []
        logging.info(
            "PlateAPI.Process: got total plate images[%d]" % len(images))
        for index, single_image in enumerate(images):
            logging.info("PlateAPI.Process: processing image[%d]" % index)
            single_chars = self.__recognize(single_image)
            char_list.append(single_chars)
            logging.info("PlateAPI.Process: done image[%d] with char[%s]" % (
                index, single_chars))
        if self._cfg.SAVE:
            logging.info("PlateAPI.Process: Swith on Save in CFGS, saving....")
            self.__save(original_image, images, char_list)
        return char_list

