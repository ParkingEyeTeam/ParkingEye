# import tensorflow
import base64
import copy
import os
import random
import time

import cv2
import imutils as imutils
from IPython.display import display
from PIL import Image
# from deepface import DeepFace
import torch
import gc
import albumentations
from albumentations import pytorch as AT
import torch
import torch.nn as nn
import numpy as np
from efficientnet_pytorch import EfficientNet
from deepface import DeepFace

# model = torch.hub.load('/home/nikita/yolov5recognition/yolov5/', 'custom',
#                        path='/home/nikita/yolov5recognition/yolov5/runs/train/exp_1/weights/best.pt', source='local')
# C:\Users\igors/.cache\torch\hub\ultralytics_yolov5_master
# model = torch.hub.load('ultralytics/yolov5', 'custom', 'weights/yolo_weights.pt')
model = torch.hub.load('C:\\Users\\igors/.cache\\torch\\hub\\ultralytics_yolov5_master', 'custom',
                       'weights/cars.pt', source='local')
model.conf = 0.4

gc.collect()
torch.cuda.empty_cache()


def is_included(bbox, point):
    if bbox[0] < point[0] < bbox[2] and bbox[1] < point[1] < bbox[3]:
        return True
    return False


_points_0 = [(77, 245), (277, 305), (507, 324), (153, 305), (215, 315), (347, 336), (422, 339), (597, 348)]
_points_1 = [(236, 193), (189, 202), (135, 228)]
_points_4 = [(59, 253), (47, 306)]
_points_3 = [(204, 136), (483, 158), (472, 145), (405, 157), (308, 219), (386, 248), (141, 279), (476, 279), (580, 314),
             (384, 394), (595, 443)]
_points_6 = [(57, 213), (494, 203), (582, 230)]
_points_5 = [(560, 37), (360, 47), (454, 44), (269, 70), (55, 160)]
_points_7 = []
_points_10 = [(554, 197), (61, 254), (195, 259), (496, 257)]
_points_11 = [(123, 179), (140, 175), (105, 183), (193, 226), (327, 242), (523, 274), (600, 294)]
_points_12 = [(188, 167), (227, 110), (269, 137), (135, 146), (429, 180), (541, 211), (132, 192), (617, 233)]
_points_14 = [(230, 178), (239, 106), (281, 131), (121, 163), (151, 145), (167, 145), (317, 161), (336, 159), (87, 176),
              (321, 187), (312, 193), (422, 268), (193, 316), (296, 353), (552, 413)]
_points_15 = [(596, 207), (620, 202), (553, 244), (413, 267), (296, 266), (237, 279), (171, 293), (111, 299),
              (507, 303), (48, 305), (401, 335), (356, 345), (176, 385), (131, 394)]
bboxes = []

cur_id = 12
_points = _points_12
img_src_dir = 'data/' + str(cur_id) + '/'
# photo_name = os.listdir(img_src_dir)[random.randint(0, len(os.listdir(img_src_dir)) - 1)]
photo_name = '23-11-2021_03-48-35_PM.jpg'
frame = cv2.imread(img_src_dir + photo_name)
frame = cv2.resize(frame, (640, 480))
# file_name = 'data/15/24-11-2021_01-48-45_PM.jpg'
# frame = cv2.imread(file_name)
w, h = (640, 480)
old_w, old_h = frame.shape[1], frame.shape[0]
frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
frame_copy = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
result = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
results = model(result)

if not results.pandas().xyxy[0].empty:
    for res in range(len(results.pandas().xyxy[0])):
        r = results.pandas().xyxy[0].to_numpy()[res]
        # print(r)
        if r[6] != 'car':
            continue
        # if not results.pandas().xyxy[0].empty:
        pad = 20

        x0 = int(r[0])
        y0 = int(r[1])
        x1 = int(r[2])
        y1 = int(r[3])
        bboxes.append((x0, y0, x1, y1))
        # if is_included((x0, y0, x1, y1), )
print(bboxes)
image = cv2.imread(img_src_dir + photo_name)
image = cv2.resize(image, (640, 480))
cnt_empty = 0
for i in range(len(_points)):
    f = 0
    cX, cY = _points[i]
    for j in range(len(bboxes)):
        if is_included(bboxes[j], _points[i]):
            f = 1
    if f == 0:
        cnt_empty += 1
        cv2.circle(image, (cX, cY), 7, (0, 255, 0), -1)
    else:
        cv2.circle(image, (cX, cY), 7, (0, 0, 255), -1)

print(len(_points), cnt_empty)
# def print_points(image, points):
#     for i in range(len(points)):
#         p = points[i]
#         cX, cY = p
#         cv2.circle(image, (cX, cY), 7, (0, 255, 0), -1)
#
#         # cv2.putText(image, "center", (cX - 20, cY - 20),
#         #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# print_points(image, _points)
cv2.imwrite('for_nikita/' + str(cur_id) + '.png', image)
# # heatmap /= np.max(heatmap)
# # cv2.imshow('test', heatmap)
# # cv2.imwrite('heatmap.png', heatmap)
# # zeros_img = np.zeros((480, 640, 3))
# find_clusters(heatmap, image)

# cv2.imwrite('heatmap_int.png', heatmap)
# if cv2.waitKey(10000) & 0xFF == ord('q'):
#     pass

# cv2.destroyAllWindows()
