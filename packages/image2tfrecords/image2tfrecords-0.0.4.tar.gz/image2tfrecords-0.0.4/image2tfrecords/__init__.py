"""
A lib create tfrecords file from images and create dataest from tfrecords.

Introduction
------------------------------
Features:

* Create tfrecords from images.
    * split the images with stratified strategy.
* Provide a interface for tensorflow DataSet API.
"""
from os import path

from . import imagedataset
from . import image2tfrecords


__version__ = "0.0.4"
