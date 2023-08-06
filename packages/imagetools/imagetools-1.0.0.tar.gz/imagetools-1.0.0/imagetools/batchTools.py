# coding=utf-8
import os


def findAllImages(root_dir, image_type):
    paths = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(image_type):
                paths.append(parent + filename)
    return paths
