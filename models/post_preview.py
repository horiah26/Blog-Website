"""Defines the PostPreview class that contains only first 200 characters of text"""

class PostPreview:
    """Defines the post attributes"""
    def __init__(self, post_id, title, text, owner, owner_username, img_id, date_created = None, date_modified = None):
        self.post_id = post_id
        self.title = title
        self.text = self.format_preview(text)
        self.owner = owner
        self.owner_username = owner_username
        self.img_id = img_id
        self.date_created = date_created
        self.date_modified = date_modified

    def format_preview(self, text):
        """Removes the last whitespace and comma if ending with a comma, adds three dots at the end"""
        text = text.rsplit(' ', 1)[0]
        if text[-1] == ",":
            text = text[:-1]
        if len(text) > 100:
            text += "..."
        return text
