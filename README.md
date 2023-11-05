# Image2Anki
Just a simple and rough version of creating Q&A in Anki from images.

![Image2Anki demonstration](https://github.com/robxcalib3r/Image2Anki/assets/34865153/91d508d8-085c-4038-9a95-fe22db0c1d5e)

## Usage
N.B. Code is still in rough form and progress in ongoing so manual editing is necessary !
1. Install required packages by -
``` pip install -r requirements.txt ```
2. Install tessaract from https://tesseract-ocr.github.io/tessdoc/Installation.html
3. Copy or remember the directory you have installed, and set the directory to ```tess_dir``` in the ```main.py```
4. Still in rough form, so you have to edit the code to change the ``` current_dir ``` to your folder of images
5. Change the ```lang``` to your preferred choice of Language. Here I used ```lang = 'bangla'``` to get bangla OCR
