#!/usr/bin/python3
import cv2
# import easyocr
from flask import Flask, render_template, request
from paddleocr import PaddleOCR
import requests
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)

file_dir = 'static/uploads/'

final_odonyms = {}


@app.before_first_request
def getData():
    root_url = 'https://bryanabsmith.com/topomapper/datafiles/'
    data_files = [
        'atsi',
        'business',
        'etc',
        'euexpl',
        'local',
        'monarchy',
        'none',
        'pol',
        'religious',
        'transplants',
        'war'
    ]

    odonyms = {}

    for theme in data_files:
        print(f'Adding {theme}...')
        contents = requests.get(f'{root_url}{theme}.json')
        to_parse = contents.json()
        for odonym in to_parse['features']:
            # print(to_parse['features']['properties']['name'])
            odonyms[
                odonym['properties']['name']
            ] = odonym['properties']['description'], \
                odonym['properties']['refs']

    print('Removing duplicates...')

    for key, value in odonyms.items():
        if value not in final_odonyms:
            final_odonyms[key] = value


@app.route('/upload', methods=['GET', 'POST'])
def uploadPic():
    '''
    Huge thanks to Nicholas Renotte's tutorial here
    https://github.com/nicknochnack/ANPRwithPython/blob/main/ANPR%20-%20Tutorial.ipynb
    '''
    # Get the file info
    upload = request.files.getlist('file')[0]

    # Name and location of the file on the server
    full_file_name = file_dir + secure_filename(upload.filename)

    # Save the uploaded file so that it can be OCR'd
    upload.save(full_file_name)

    # Read in the image
    img = cv2.imread(full_file_name)

    # Convert it to greyscale
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # https://github.com/nicknochnack/DrugLabelExtraction-/blob/main/Paddle%20OCR%20Tutorial.ipynb
    ocr_model = PaddleOCR(lang='en')
    result = ocr_model.ocr(grey)
    print(result)

    full_text = ''
    for res in result:
        full_text += ' ' + res[1][0]

    os.remove(full_file_name)

    for odonym in final_odonyms:
        if full_text.lower().find(odonym.split(' ')[0].lower()) > -1:
            # return f'{odonym} St, named for {fake_names[odonym]}.'
            return f'''<blockquote class="blockquote">
                <h1 class="display-6" style="color: #0dcaf0;">{odonym}</h1>
                <p class="mb-0">{final_odonyms[odonym][0]}</p>
                <p></p>
                <p><small>{final_odonyms[odonym][1]}</small></p>
            </blockquote>'''

    return 'Nothing found. Try again with a different picture.'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
