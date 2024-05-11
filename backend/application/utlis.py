import os
from werkzeug.utils import secure_filename
from PIL import Image

def save_image(image):
    if isinstance(image,str):
        return 'static/shows/'+ image

    img = Image.open(image)
    img = img.resize((800,800))
    filename = secure_filename(image.filename)
    resized_name = 'resized_' + filename 
    resized_path = os.path.join('static/shows/', resized_name)
    img.save(resized_path)
    return resized_path





    # filename = secure_filename(image.filename)
    # path = os.path.join('static/shows/',filename)

    # print(path)
    # image.save(path)