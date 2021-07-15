"""Defines the PostPreview class that contains only first 200 characters of text"""

class PostPreview:
    """Defines the post attributes"""
    def __init__(self, post):
        self.post_id = post.post_id
        self.title = post.title
        self.text = self.preview(post.text)
        self.owner = post.owner
        self.date_created = post.date_created
        self.date_modified = post.date_modified

    def preview(self, text):
        """Selects only the first 180 chars then removes last whitespace or comma"""
        text = text[0:180]
        text = text.rsplit(' ', 1)[0]
        if text[-1] == ",":
            text = text[:-1]
        text += "..."
        return text
