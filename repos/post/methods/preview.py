def preview(text):
    text = text[0:190];
    if len(text) > 150:
        text = text.rsplit(' ', 1)[0] 
        text = text.rsplit(',', 1)[0] 
        text = text + "..."

    return text