"""Handles images for posts"""
import os
import copy
from os import path, listdir
from os.path import isfile, join

from flask import current_app

class ImageRepo():
    """Handles images for posts"""
    def __init__(self):
        self.images = []
        self.path = current_app.config['UPLOAD_FOLDER']         
        self.update_image_list()
        self.extension = '.png'

    def save(self, image) -> int:
        """Saves image to uploads folder and returns an id"""
        self.update_image_list()
        if image:
            exists_id = self.check_if_exists(image)
            if exists_id is not None:
                return exists_id

            img_id = self.get_id()
            image.save(os.path.join(self.path, str(img_id) + self.extension))
            return img_id

        return 0

    def check_if_exists(self, image):
        """Checks if an image with the same name and size (kb) exists in uploads folder"""
        image.seek(0, os.SEEK_END)
        image_size = image.tell()
        image.seek(0)

        filename = image.filename.rsplit('.', 1)[0]
        if filename.isdigit() and int(filename) in self.images:
            if image_size == os.path.getsize(self.path + '/' + filename + self.extension):
                return int(filename)
        return None

    def allowed_file(self, filename):
        """Checks the image file has the correct extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def get_id(self):
        """Returns id for new uploaded picture"""
        self.update_image_list()
        if len(self.images) == 0:   
            return 0         
        return max(self.images) + 1

    def update_image_list(self):
        """Reads all images from upload folders and keeps their names as integers in a list"""
        self.images = []
        files_in_uploads = [f.rsplit('.', 1)[0] for f in listdir(self.path) if isfile(join(self.path, f)) and self.allowed_file(f)]
        for image_nr in files_in_uploads:
            if image_nr:
                self.images.append(int(image_nr))

    def delete(self, img_id):
        """Deletes image by id"""
        del_path = self.path + '/' + str(img_id) + self.extension
        if os.path.exists(del_path):
             os.remove(del_path)
