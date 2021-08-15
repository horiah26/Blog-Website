"""Handles images for posts"""
import os
import copy
from os import path, listdir
from os.path import isfile, join

from flask import current_app

class ImageRepo():
    def __init__(self):
        self.path = current_app.config['UPLOAD_FOLDER']         
        self.update_image_list()
        self.extension = '.png'

    def save(self, image):
        self.update_image_list()
        if image:
            exists_id = self.check_if_exists(image)
            if exists_id:
                return exists_id

            img_id = self.get_id()
            print(image)
            image.save(os.path.join(self.path, str(img_id) + self.extension))
            return img_id

        return 0

    def check_if_exists(self, image):
        image.seek(0, os.SEEK_END)
        image_size = image.tell()
        image.seek(0)

        filename = image.filename.rsplit('.', 1)[0]
        if filename.isdigit() and int(filename) in self.images:
            if image_size == os.path.getsize(self.path + '/' + filename + self.extension):
                return filename
        return None

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def get_id(self):
        self.update_image_list()
        if len(self.images) == 0:   
            return 0         
        return max(self.images) + 1

    def get(self, img_id):
        pat = self.path + '/'
        filepath = os.path.join(self.path + '/', str(img_id) + self.extension)
        return open(filepath, 'r')

    def update_image_list(self):
        self.images = []
        files_in_uploads = [f.rsplit('.', 1)[0] for f in listdir(self.path) if isfile(join(self.path, f)) and self.allowed_file(f)]
        for image_nr in files_in_uploads:
            if image_nr:
                self.images.append(int(image_nr))

    def delete(self, img_id):
        del_path = self.path + '/' + str(img_id) + self.extension
        if os.path.exists(del_path):
             os.remove(del_path)
