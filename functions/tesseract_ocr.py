from imutils.object_detection import non_max_suppression
from PIL import Image
from pytesseract import Output
import numpy as np 
import pytesseract
import cv2
import os
import math

# Create class
class Tesseract_ocr:
    def __init__(self, img_path, preprocess="thresh", min_confidence=0.5):
        self.img_path = img_path
        self.preprocess = preprocess
        self.min_confidence = min_confidence

    
    def start_ocr(self):
        # set the tesseract path in the script before calling
        pytesseract.pytesseract.tesseract_cmd = os.path.abspath(os.getcwd()) + r'/Tesseract-OCR/tesseract.exe'

        #------------------------------------------------------------------
        # image path
        img_path = self.img_path
        preprocess = "thresh"

        # load the input image and grab the image deimensions
        image = cv2.imread(img_path)

        # convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Check to see if we should apply thresholding to preprocess the image
        if preprocess == "thresh":
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # check to see if median blurring should be done to remove noise
        elif preprocess == "blur":
            gray = cv2.medianBlur(gray, 3)
            
        temp_path = os.path.abspath(os.getcwd()) + r'/temp'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        filename = os.path.abspath(os.getcwd()) + r"/temp/{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        img_gray = cv2.imread(filename)
        
        #------------------------------------------------------------------
        # initialize the list of results
        results = []

        # use oytesseract get image data
        d = pytesseract.image_to_data(img_gray, output_type=Output.DICT)
        n_boxes = len(d['level'])

        origW = d['width'][0]
        origH = d['height'][0]

        for i in range(n_boxes):
            # get text data
            text = d['text'][i]
            conf = d['conf'][i]
            # get text position data
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])

            # set ratio of position to original pic
            ratio_sx = x / origW
            ratio_sy = y / origH
            ratio_ex = (x + w) / origW
            ratio_ey = (y + h) / origH

            diff_w = origW - w
            diff_h = origH - h

            if diff_w > 5 and diff_h > 5:
                if text != "" and conf != -1:  
                    results.append(((ratio_sx, ratio_sy, ratio_ex, ratio_ey), text))
        return results