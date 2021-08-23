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
        self.images = []
        self.path = current_app.config['UPLOAD_FOLDER'] + '/profile/'
        self.update_image_list()

    def save(self, image) -> int:
        """Saves image to uploads folder and returns an id"""
        self.update_image_list()
        if image:
            img_id = self.get_id()
            image.save(os.path.join(self.path, str(img_id) + self.extension))
            return img_id

        return 0

    def allowed_file(self, filename):
        """Checks the image file has the correct extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

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
    @inject
    def delete_unused(self, user_repo = Provide['user_repo']):
        """Deletes unused images from uploads folder"""
        if current_app.config['DB_TYPE'] in ['db', 'alchemy']:
            self.update_image_list()
            used_images_list = set(map(lambda x: x.img_id, user_repo.get_all()))

            for img in self.images:
                if img not in used_images_list:
                    self.delete(img)

            self.update_image_list()

    def delete(self, img_id):
        """Deletes image by id"""
        del_path = self.path + '/' + str(img_id) + self.extension
        if os.path.exists(del_path):
            os.remove(del_path)
