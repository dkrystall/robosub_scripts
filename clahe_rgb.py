'''
Applies CLAHE to color images
Source: https://stackoverflow.com/questions/25008458/how-to-apply-clahe-on-rgb-color-images
'''

import sys
import cv2

img_path = sys.argv[1]
img_name = img_path.split('/')[-1]

bgr = cv2.imread(img_path)

lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)

lab_planes = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

lab_planes[0] = clahe.apply(lab_planes[0])

lab = cv2.merge(lab_planes)

bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

cv2.imwrite('clahe_rgb_{}'.format(img_name), bgr)
