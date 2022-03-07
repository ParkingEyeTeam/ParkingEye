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
ids = [0, 1, 3, 4, 5, 6, 7, 10, 11, 12, 14, 15]
cap = cv2.VideoCapture(0)
cur_id = 12
# while cap.isOpened():
#     # читаем кадр из видео
#     ret, frame = cap.read()
img_src_dir = 'data/' + str(cur_id) + '/'
if not os.path.exists('data/' + str(cur_id) + '_infer'):
    os.mkdir('data/' + str(cur_id) + '_infer')

img_dst_dir = 'data/' + str(cur_id) + '_infer/'

heatmap = np.zeros((480, 640), dtype=np.int8)
for file in os.listdir(img_src_dir):

    frame = cv2.imread(img_src_dir + file)
    # print(file)
    t = time.time()
    # print(file)
    # cv2.imshow('123', frame)
    # if cv2.waitKey(1000) & 0xFF == ord('q'):
    #     break
    # frame = cv2.imread('/home/nikita/yolov5recognition/datasets/rfd/test_1_photo_per_human/afraid/AF03AFS.JPG')
    # frame_copy = copy.deepcopy(frame)
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
            pad = 30

            x0 = int(r[0])
            y0 = int(r[1])
            x1 = int(r[2])
            y1 = int(r[3])

            center_x = (x0 + x1) // 2
            center_y = (y1 + y0) // 2
            heatmap[center_y - pad:center_y + pad, center_x - pad:center_x + pad] += 1
            # cv2.putText(frame, confidence, (x0 + 20, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            # cv2.putText(frame, emotion, (x0, y0 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            # cv2.imshow("crop", crop)
            # print(1)
    # cv2.imshow("Demo", frame)

    frame = cv2.resize(frame, (old_w, old_h))
    cv2.imwrite(img_dst_dir + file, frame)


def find_clusters(cur_heatmap, image, thresh_por=15):
    cur_mask = np.where(cur_heatmap > thresh_por, 1, 0).astype(np.uint8)

    n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cur_mask)
    cur_points = []
    size_thresh = 1
    appended = False
    points = []
    for j in range(1, n_labels):
        if stats[j, cv2.CC_STAT_AREA] >= size_thresh:
            # print(stats[i, cv2.CC_STAT_AREA])
            x = stats[j, cv2.CC_STAT_LEFT]
            y = stats[j, cv2.CC_STAT_TOP]
            w = stats[j, cv2.CC_STAT_WIDTH]
            h = stats[j, cv2.CC_STAT_HEIGHT]
            cX = int(x + w // 2)
            cY = int(y + h // 2)
            points.append((cX, cY))
            cv2.circle(image, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(image, "center", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    print(points)
    # print(time.time() - t)
# _points_3 = [(204, 136), (483, 158), (472, 145), (405, 157), (308, 219), (386, 248), (141, 279), (476, 279), (580, 314),
#            (384, 394), (595, 443)]


# def print_points(image, points):
#     for i in range(len(points)):
#         p = points[i]
#         cX, cY = p
#         cv2.circle(image, (cX, cY), 7, (0, 255, 0), -1)
#
#         # cv2.putText(image, "center", (cX - 20, cY - 20),
#         #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

photo_name = os.listdir(img_src_dir)[random.randint(0, len(os.listdir(img_src_dir))-1)]
image = cv2.imread(img_src_dir + photo_name)
image = cv2.resize(image, (640, 480))
find_clusters(heatmap, image)
# # print_points(image, _points)
cv2.imwrite('clusters_' + str(cur_id) + '.png', image)
# # heatmap /= np.max(heatmap)
# # cv2.imshow('test', heatmap)
# # cv2.imwrite('heatmap.png', heatmap)
# # zeros_img = np.zeros((480, 640, 3))


# cv2.imwrite('heatmap_int.png', heatmap)
# if cv2.waitKey(10000) & 0xFF == ord('q'):
#     pass

# cv2.destroyAllWindows()
