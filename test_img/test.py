#!/usr/bin/python3

import os

import easyocr

list_files = os.listdir('.')
list_files.remove('test.py')

test_files = len(list_files)
test_count_right = 0

for file in list_files:
    name = file.split('.')[0]

    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(file)

    if result.find(name) > 0:
        print('\u2713', name)
        test_count_right += 1
    else:
        print('\u2717', name)

print(f'Total Passed: {test_count_right}/{test_files}.')
print(f'Coverage: {(test_count_right/test_files)*100}.')
