#!/usr/bin/python3
from typing import final
import easyocr
from flask import Flask, render_template, request
import requests
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)

file_dir = 'static/uploads/'

final_odonyms = {}


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
            odonyms[odonym['properties']['name']] = odonym['properties']['description'], odonym['properties']['refs']

    print('Removing duplicates...')

    for key, value in odonyms.items():
        if value not in final_odonyms:
            final_odonyms[key] = value


@app.route('/upload', methods=['GET', 'POST'])
def uploadPic():
    '''
        To-do:
        1. Run EasyOCR on the picture
            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.readtext(img)
            for x in result:
                print(x[1])
        2. Look up info in the database/json file
        3. Render template with info
    '''

    # Get the file info
    upload = request.files.getlist('file')[0]

    # Name and location of the file on the server
    full_file_name = file_dir + secure_filename(upload.filename)
    
    # Save the uploaded file so that it can be OCR'd
    upload.save(full_file_name)

    # Thanks to Nicholas Renotte for the EasyOCR lines (https://www.youtube.com/watch?v=ZVKaWPW9oQY)
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(full_file_name)
    full_text = ''
    for x in result:
        full_text += ' ' + x[1]

    os.remove(full_file_name)

    for odonym in final_odonyms:
        print(odonym.split(' ')[0].lower() + ' ' + odonym.split(' ')[1][:1].lower())
        #if full_text.split(' ')[0].lower().find(full_text) > 0:
        if full_text.lower().find(odonym.split(' ')[0].lower() + ' ' + odonym.split(' ')[1][:1].lower()) > 0:
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
    getData()
    app.run(host='0.0.0.0', debug=True)