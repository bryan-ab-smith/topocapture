#!/usr/bin/python3

from timeit import default_timer
import logging
import os

import easyocr

# https://stackoverflow.com/questions/27647077/fully-disable-python-logging
# This disable the default logging that is output by EasyOCR which interferes with the printed messages.
logging.disable(logging.CRITICAL)

# Get the list of test pictures
list_files = os.listdir('.')

# Remove the test script
list_files.remove('test.py')

# Sort the list of files
list_files.sort()

# Get the number of test pictures
test_files = len(list_files)

# Set a counter for how many of the tests pass
test_count_right = 0

print(f'Testing OCR. Found {test_files} test files.')

# Get a start time
start = default_timer()

# Current picture number
cur_pic = 1

# For each file in the list...
for file in list_files:
    # Is the file found? Default to no
    found = False

    # Get the name of the street in the file
    name = file.split('.')[0]

    # Hold the confidence value
    confidence = 0.0

    # Print that we are setting up the reader
    print(f'Setting up reader for {file}...         ', end='\r')

    # Set up an instance of the easyocr reeader
    reader = easyocr.Reader(['en'], gpu=False)

    # Tell the user that it's analysing the file
    print(f'Analysing {file}, {cur_pic} of {test_files}...              ', end='\r')

    # Analyse the file
    result = reader.readtext(file)

    # For each word in the analysis
    for text in result:
        # Check to see if the word in the result equals the name of the file
        if text[1].lower().find(name.lower()) > -1:
            # Set found to true
            found = True
            # Get the confidence value
            confidence = text[2]
    # If found is true
    if found == True:
        # Print that the word was found, with the confidence
        print('\u2713', name, '(Confidence:', str(confidence) + ')                ', end='\r')
        # Add one to the "passed/right" counter
        test_count_right += 1
    else:
        # Print that the word wasn't found
        print('\u2717', name, '                ', end='\r')
    # Move to the next line
    print('')
    cur_pic += 1
# Get the time after the analyses are done
end = default_timer()

# Print how many were passed
print(f'Total Passed: {test_count_right}/{test_files}.')
# Print the passed as a percentage
print(f'Coverage: {int((test_count_right/test_files)*100)}%.')
# Print how long it took to run the tests
print(f'Time to Run Tests: {round(end-start, 2)} seconds.')
