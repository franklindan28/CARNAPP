import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# load image
img = cv2.imread("image.jpg");

# grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

# canny
canned = cv2.Canny(gray, 100, 200);

# dilate to close holes in lines
kernel = np.ones((5,5),np.uint8)
mask = cv2.dilate(canned, kernel, iterations = 0);

# find contours
# Opencv 3.4, if using a different major version (4.0 or 2.0), remove the first underscore
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

# find big contours
biggest_cntr = None;
biggest_area = 0;
for contour in contours:
    area = cv2.contourArea(contour);
    if area > biggest_area:
        biggest_area = area;
        biggest_cntr = contour;

# draw contours
crop_mask = np.zeros_like(mask);
cv2.drawContours(crop_mask, [biggest_cntr], -1, (255), -1);

# fill in holes
# inverted
inverted = cv2.bitwise_not(crop_mask);

# contours again
contours, _ = cv2.findContours(inverted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

# find small contours
small_cntrs = [];
for contour in contours:
    area = cv2.contourArea(contour);
    if area < 20000:
        print(area);
        small_cntrs.append(contour);

# draw on mask
cv2.drawContours(crop_mask, small_cntrs, -1, (255), -1);

# opening + median blur to smooth jaggies
crop_mask = cv2.erode(crop_mask, kernel, iterations = 1);
crop_mask = cv2.dilate(crop_mask, kernel, iterations = 1);
crop_mask = cv2.medianBlur(crop_mask, 5);

# crop image
crop = np.zeros_like(img);
crop[crop_mask == 255] = img[crop_mask == 255];

# show
cv2.imshow("original", img);
cv2.imshow("gray", gray);
cv2.imshow("canny", canned);
cv2.imshow("mask", crop_mask);
cv2.imshow("cropped", crop);
#cv2.waitKey(0);
text = pytesseract.image_to_string(img)
print(text)
cv2.waitKey(0)
cv2.destroyAllWindows()