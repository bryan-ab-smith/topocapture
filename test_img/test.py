#!/usr/bin/python3

from timeit import default_timer
import logging
import os

import easyocr

# https://stackoverflow.com/questions/27647077/fully-disable-python-logging
logging.disable(logging.CRITICAL)

list_files = os.listdir('.')
list_files.remove('test.py')

test_files = len(list_files)
test_count_right = 0

print(f'Testing OCR. Found {test_files} test files.')

start = default_timer()
for file in list_files:
    found = False
    name = file.split('.')[0]
    confidence = 0.0

    print(f'Setting up reader for {file}...         ', end='\r')
    reader = easyocr.Reader(['en'], gpu=False)
    print(f'Analysing {file}...              ', end='\r')
    result = reader.readtext(file)

    for text in result:
        if text[1].lower().find(name.lower()) > -1:
            found = True
            confidence = text[2]
    if found == True:
        print('\u2713', name, '(Confidence:', str(confidence) + ')                ', end='\r')
        test_count_right += 1
    else:
        print('\u2717', name, '                ', end='\r')
    print('')
end = default_timer()

print(f'Total Passed: {test_count_right}/{test_files}.')
print(f'Coverage: {(test_count_right/test_files)*100}.')
print(f'Time to Run Tests: {end-start}')
