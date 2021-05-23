## Topocapture

More to come, work (very much) in progress.

### Status

As of 22/05/2021, it works albeit slowly unless you tweak the EasyOCR reader in uploadPic() to use a GPU.

### Development

1. Setup the dependencies:

        $ npm install && mv node_modules/ static/
        $ python3 -m pip install -r requirements.txt

2. Run the local version:

        $ python3 app.py

### Testing

Run the test.py script in the test_img/ folder. This will test the OCR against a series of test pictures. Ideally, you get 100% coverage but decide for yourself what an acceptable limit is.

The pictures are purposefully clear/blurry, from day/night, and inclusive of extra text.

### License

Copyright 2021 Bryan Smith

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
Software, and to permit persons to whom the Software is furnished to do so, subject 
to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.