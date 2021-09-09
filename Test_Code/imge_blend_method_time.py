import time

import cv2
import numpy
import numpy as np

img = cv2.imread('./test_clip/input_frames/frame151.png', 1)
img2 = cv2.imread('./test_clip/input_frames/frame133.png', 1)
h0, h1, x0, x1 = 300, 800, 400, 1580
# img[h:h1,x:x1,:]=img2[h:h1,x:x1,:]
# cv2.imwrite('结果.png',img)
h, w, c = img.shape
mask = np.zeros((h, w, 3), dtype=np.uint8)
# mask = np.zeros(img.shape[:2], dtype=np.uint8)
mask[h0:h1, x0:x1, :] = 1

# gray_mask= cv2.cvtColor(mask.repeat(3,axis=2), cv2.COLOR_BGR2GRAY)
# ret, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
mask_one_channel = mask[:, :, 0]
T1 = time.time()
for i in range(90):

    res = (img2 & mask) | ((~mask) & img)

    # res1 = cv2.bitwise_and(img2, img2, mask=mask_one_channel)
    # res1 = cv2.bitwise_and(img2, mask)

    # res2 = cv2.bitwise_and(img, img, mask=1 - mask_one_channel)
    # res2 = cv2.bitwise_and(img, 1 - mask)
    # res = cv2.bitwise_or(res1, res2)
print('90帧 cv2与操作', time.time() - T1)
cv2.imwrite('与操作cv2.png', res)

T1 = time.time()
for i in range(90):
    test = img2 * mask + (1 - mask) * img
print('90帧按元素相乘再相加', time.time() - T1)
cv2.imwrite('元素相乘.png', test)

T1 = time.time()
for i in range(90):
    img[h0:h1, x0:x1, :] = img2[h0:h1, x0:x1, :]
print('90帧取值操作', time.time() - T1)
cv2.imwrite('取值操作.png', img)
