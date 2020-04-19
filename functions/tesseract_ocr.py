from imutils.object_detection import non_max_suppression
from PIL import Image
import numpy as np 
import pytesseract
import cv2
import os
import math

def decode_predictions(scores, geometry, min_confidence):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the Geometrical
        # data used to derive potential bounding box coordinates that 
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability
            # ignore it
            if scoresData[x] < min_confidence:
                continue
            
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            
            # use the geometry volumn to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            
            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY + (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            
            
            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
            
    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


# Create class
class Tesseract_ocr:
    def __init__(self, img_path, preprocess="thresh", min_confidence=0.5, padding=0):
        self.img_path = img_path
        self.preprocess = preprocess
        self.min_confidence = min_confidence
        self.padding = padding

    
    def start_ocr(self):
        # set the tesseract path in the script before calling
        pytesseract.pytesseract.tesseract_cmd = os.path.abspath(os.getcwd()) + r'\Tesseract-OCR\tesseract.exe'

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
            
        temp_path = os.path.abspath(os.getcwd()) + r'\temp'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        filename = os.path.abspath(os.getcwd()) + r"\temp\{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        img_gray = cv2.imread(filename)

        orig = img_gray.copy()
        (origH, origW) = img_gray.shape[:2]

        # get image height and width
        (w, h) = Image.open(filename).size
        newW = 320*5# round(w/32)*32
        newH = 320*5# round(h/32)*32

        # set the new width and heigh and then determine the ratio in change
        # for both the width and heigh
        rW = origW / float(newW)
        rH = origH / float(newH)

        # resize the image and grab the new image dimensions
        img_gray = cv2.resize(img_gray, (newW, newH))
        (H, W) = img_gray.shape[:2]

        #------------------------------------------------------------------
        # EAST text detector path
        east_path = os.path.abspath(os.getcwd()) + r'\functions\frozen_east_text_detection.pb'
        # define the two output layer names for the EAST detector model that
        # we are interested in -- the first is the output probabilities and the 
        # second can be used to derive the bouding box coordinates of text
        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"
        ]

        # load the pre-trained EAST text detector
        print("[INFO] loading EAST text detector...")
        net = cv2.dnn.readNet(east_path)

        # construct a blob from the image and then perform a forward pass of 
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(img_gray, 1.0, (W,H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        # decode the predictions, then apply non-maxima suppression to
        # suppress weak, overlapping bounding boxes
        (rects, confidences) = decode_predictions(scores, geometry, self.min_confidence)
        boxes = non_max_suppression(np.array(rects), probs=confidences)

        #------------------------------------------------------------------
        # initialize the list of results
        results = []

        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective ratios
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            
            # in order to obtain a better OCR of the text we can potentially
            # apply a bit of padding surrounding the bounding box -- here we
            # are computing the deltas in both the x and y directions
            dX = int((endX - startX) * self.padding)
            dY = int((endY - startY) * self.padding)
            
            # apply padding to each side of the bounding box, respectively
            startX = max(0, startX - dX)
            startY = max(0, startY - dY)
            endX = min(origW, endX + (dX * 2))
            endY = min(origH, endY + (dY * 2))
            
            # extract the actual padded ROI
            roi = orig[startY:endY, startX:endX]
            
            # in order to apply Tesseract v4 to OCR text we must supply
            # (1) a language, (2) an OEM flag of 4, indeicating that the
            # we wish to use the LSTM neural net model for OCR, and finally
            # (3) an OEM value, in this case, 7 which implies that we are
            # treating the ROI as a single line of text
            config = ("-l eng --oem 1 --psm 7")
            text = pytesseract.image_to_string(roi, config=config)

            # Get each side by percentage
            p_startX = startX / origW
            p_startY = startY / origH
            p_endX = endX / origW
            p_endY = endY / origH

            p_startX = round(p_startX, 3)
            p_startY = round(p_startY, 3)
            p_endX = round(p_endX, 3)
            p_endY = round(p_endY, 3)
            
            # add the bounding box coordinates and OCR'd text to the list
            # of results
            results.append(((p_startX, p_startY, p_endX, p_endY), text))
        
        results = sorted(results, key=lambda r: r[0][1])

        return results