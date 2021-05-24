#!/usr/bin/python3

import logging
import os

import easyocr

list_files = os.listdir('.')
list_files.remove('test.py')

test_files = len(list_files)
test_count_right = 0

for file in list_files:
    found = False
    name = file.split('.')[0]
    confidence = 0.0

    print(f'Analysing {file}...')
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(file)

    for text in result:
        if text[1].lower().find(name.lower()) > -1:
            found = True
            confidence = text[2]
    if found == True:
        print('\u2713', name, '--> Confidence:', confidence)
        test_count_right += 1
    else:
        print('\u2717', name)

print(f'Total Passed: {test_count_right}/{test_files}.')
print(f'Coverage: {(test_count_right/test_files)*100}.')
