# Var. 7


import cv2


img = cv2.imread('images/7.jpg')
reflected_img = cv2.flip(img, 1)
res_img = cv2.rotate(reflected_img, cv2.ROTATE_180)

cv2.imwrite('images/71.jpg', reflected_img)
cv2.imwrite('images/72.jpg', res_img)
