#!/usr/bin/python3
import easyocr
from flask import Flask, render_template, request
from numpy.core.numeric import full
import requests
from werkzeug.utils import secure_filename

import json
import os

app = Flask(__name__)

file_dir = 'static/uploads/'

def getData():
    '''root_url = 'https://bryanabsmith/topomapper/datafiles/'
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

    for data in data_files:
        print(requests.get(f'{root_url}{data}.json'))
    '''




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

    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(full_file_name)
    full_text = ''
    for x in result:
        full_text += ' ' + x[1]

    os.remove(full_file_name)

    fake_names = {
        'Murray': 'Fakey Murray, mayor in 2019.',
        'Flinders': 'Mathew Flinders, explorer',
        'Sturt': 'Another surveyor'
    }

    for odonym in fake_names:
        if full_text.lower().find('murray') > 0:
            # return f'{odonym} St, named for {fake_names[odonym]}.'
            return f'''<blockquote class="blockquote">
                <p class="mb-0">{fake_names[odonym]}</p>
                <br \>
                <footer class="blockquote-footer">{odonym}</cite></footer>
            </blockquote>'''
    
    return full_text

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    getData()
    app.run(debug=True)