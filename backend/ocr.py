from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import os

DEBUG_MODE=False
model=load_model('modelwts2.h5')

arr_result = ['0','1','2','3','4','5','6','7','8','9',
              'A','B','C','D','E','F','G','H','I','J','K',
              'L','M','N','O','P','Q','R','S','T','U','V',
              'W','X','Y','Z'
             ]

def extract_text(filepath):
    inp_img = cv2.imread(filepath)
    img = inp_img.copy()
    denoised = cv2.fastNlMeansDenoising(inp_img, h=7)
    gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    predicted_str = 'test'
    h_list = [];
    contours = sort_contours(contours)[1:]
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 290:
            h_list.append([x, y, w, h])
    for hl in h_list:
        x, y, w, h = hl
        test_image = gray[y:y + h, x:x + w]
        show_img(test_image)
        test_image = cv2.resize(test_image.copy(), (64, 64), interpolation=cv2.INTER_AREA)
        test_image = (image.img_to_array(test_image)) / 255
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        # np.reshape(result, 36)
        # maxval = np.amax(result)
        # index = np.where(result == maxval)
        # rs = arr_result[index[1][0]]
        # predicted_str = predicted_str + rs
    os.remove(filepath)
    return predicted_str

def show_img(img,name="image"):
    if(DEBUG_MODE):
        cv2.imshow(name,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def sort_contours(cnts):
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][0], reverse=False))
    return cnts
