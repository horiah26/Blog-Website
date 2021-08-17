"""Handles images for posts"""
import os
from flask import current_app
from dependency_injector.wiring import inject, Provide

class ImageRepoMemory():
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
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])

    def get_id(self):
        """Returns id for new uploaded picture"""
        if len(self.images) == 0:
            return 0
        return max(self.images) + 1

    @inject
    def delete_unused(self, post_repo = Provide['post_repo']):
        """Deletes unused images from uploads folder"""
        if current_app.config['DB_TYPE'] in ['db', 'alchemy']:
            used_images_list = set(map(lambda x: x.img_id, post_repo.get_all()))

            for img in self.images:
                if img not in used_images_list:
                    self.delete(img)

    def delete(self, img_id):
        """Deletes image by id"""
        del_path = self.path + '/' + str(img_id) + self.extension
        if os.path.exists(del_path):
            os.remove(del_path)
