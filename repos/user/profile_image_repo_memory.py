"""Handles images for user profiles"""
import os
from os import listdir
from os.path import isfile, join

from flask import current_app
from dependency_injector.wiring import inject, Provide

class ProfileImageRepo():
    """Handles images for posts"""
    def __init__(self):
        self.extension = '.png'
        self.images = [0]

    def save(self, image) -> int:
        """Saves image to uploads folder and returns an id"""
        if image:
            img_id = self.get_id()
            self.images.append(img_id)
            return img_id
        return 0

    def allowed_file(self, filename):
        """Checks the image file has the correct extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

    def get_id(self):
        """Returns id for new uploaded picture"""
        if len(self.images) == 0:
            return 0
        return max(self.images) + 1
