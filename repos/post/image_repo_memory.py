"""Handles images for posts"""

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
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

    def get_id(self):
        """Returns id for new uploaded picture"""
        if len(self.images) == 0:
            return 0
        return max(self.images) + 1

    def delete_unused(self):
        """Unused, deleting unused images is not tested"""
