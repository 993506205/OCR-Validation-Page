from imutils.object_detection import non_max_suppression
from PIL import Image
from pytesseract import Output
import numpy as np 
import pytesseract
import cv2
import os
import math
from sys import platform


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

# sharpen kernel
def sharpen_kernel(image):
    sk = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(image, -1, sk)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((7,7),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# blur image
def blur(image):
    return cv2.blur(image,(3,3))

# median blur
def median_blur(image):
    return cv2.medianBlur(image, 21)

# normalize image
def normalize(diff, norm):
    cv2.normalize(diff, norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)


# Create class
class Tesseract_ocr:
    def __init__(self, img_path, preprocess="thresh", min_confidence=0.5):
        self.img_path = img_path
        self.preprocess = preprocess
        self.min_confidence = min_confidence

    
    def start_ocr(self):
        if platform == "win32":
            # set the tesseract path in the script before calling
            pytesseract.pytesseract.tesseract_cmd = os.path.abspath(os.getcwd()) + r'/Tesseract-OCR/tesseract.exe'

        #------------------------------------------------------------------
        # image path
        img_path = self.img_path
        # preprocess = "thresh"

        # load the input image and grab the image deimensions
        image = cv2.imread(img_path)
        
        # dilated the image to get rid of the text
        dilated_img = dilate(image)
        
        # median blur the reuslt to get background
        bg_img = median_blur(dilated_img)
        
        diff_img = 255-cv2.absdiff(image, bg_img)
        norm_img = diff_img.copy()
        normalize(diff_img, norm_img)

        # preprocessing image
        gray = get_grayscale(norm_img)
        # noise = remove_noise(gray)
        # blur = blur_image(noise)
        sharpen = sharpen_kernel(gray)
        thresh = thresholding(sharpen)
        normalize(thresh, thresh)

            
        temp_path = os.path.abspath(os.getcwd()) + r'/temp'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        filename = os.path.abspath(os.getcwd()) + r"/temp/{}.png".format(os.getpid())
        cv2.imwrite(filename, thresh)

        img_preprocessing = cv2.imread(filename)
        
        #------------------------------------------------------------------
        # initialize the list of results
        results = []

        # use oytesseract get image data
        d = pytesseract.image_to_data(img_preprocessing, output_type=Output.DICT)
        n_boxes = len(d['level'])

        origW = d['width'][0]
        origH = d['height'][0]

        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
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
                    if text != "" and not text.isspace():
                        results.append(((ratio_sx, ratio_sy, ratio_ex, ratio_ey), text))
        return results