# -*- coding=utf8 -*-
import os
import sys
sys.path.append(".\\")
import argparse
from api import PlateAPI
from sqldb import DbManager

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='ULPR demo')
    parser.add_argument('--cfg_filepath', dest='cfg_filepath',
                        help='config file', default=".\\cfgs\\easypr.yml", type=str)
    parser.add_argument('--image_path', dest='image_path',
                        help='image path', default=".\\data\\test.jpg", type=str)
    args = parser.parse_args()
    return args





if __name__ == "__main__":
    args = parse_args()
    plate_api = PlateAPI(cfg_filepath=args.cfg_filepath)
    chars = plate_api.process(args.image_path)
    db = DbManager()
    db.create_table()
    for i in chars:
        db.insert_info(i)
    print (chars)

