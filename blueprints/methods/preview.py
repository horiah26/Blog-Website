def preview(text):
    text = text[0:500];
    text = text.rsplit(' ', 1)[0] 
    text = text + "..."

    return text