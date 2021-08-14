"""Handles images for posts"""
import os
from os import path, listdir
from os.path import isfile, join

from PIL import Image
from flask import current_app

class ImageRepo():
    def __init__(self):
        self.path = current_app.config['UPLOAD_FOLDER']         
        self.update_image_list()

    def save(self, image):
        if image:
            image.save(os.path.join(self.path, str(self.get_id()) + '.png'))

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def get_id(self):
        if len(self.images) == 0:   
            return 0         
        return max(self.images) + 1

    def get(self, img_id):
        pat = self.path + '/'
        filepath = os.path.join(self.path + '/', str(img_id) + '.png')
        return open(filepath, 'r')

    def update_image_list(self):
        self.images = []
        files_in_uploads = [f.rsplit('.', 1)[0] for f in listdir(self.path) if isfile(join(self.path, f)) and self.allowed_file(f)]
        for image_nr in files_in_uploads:
            if image_nr:
                self.images.append(int(image_nr))

    def delete(self, img_id):
        del_path = self.path + '/' + str(img_id) + '.png'
        if os.path.exists(del_path):
             os.remove(del_path)