import copy
import time

import cv2
import numpy as np

from detection_model import DetectionModel
from my_tracker import Tracker
from drawing import MyAnnotator


def find_clusters(cur_heatmap, thresh_por=30):
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
    # print(points)
    return points


model = DetectionModel()

tracker = Tracker()
t = time.time()
cap = cv2.VideoCapture('C:\\Users\\igors\\Videos\\test_3.mp4')
cur = 0
heatmap = np.zeros((1080, 1920), dtype=int)
max_frames = 1000
first_img = None
while cap.isOpened():
    ret, frame = cap.read()
    if first_img is None:
        first_img = copy.deepcopy(frame)
    if not ret:
        break
    cur += 1
    if cur % 5 != 0:
        continue
    result = model.predict(frame)
    parsed_res = DetectionModel.parse_result(result)
    dets = [pred.bbox for pred in parsed_res]

    np_dets = np.array(dets)

    tracks = tracker.track(np_dets)
    tracks = [list(map(int, track)) for track in tracks]
    for track in tracks:
        start = (track[0], track[1])
        end = (track[2], track[3])
        _id = str(track[4])
        MyAnnotator.rectangle(frame, start, end)
        MyAnnotator.put_text(frame, _id, (start[0], start[1]))
    cv2.imshow('test', frame)
    # bboxes = [list(map(int, track[:4])) for track in tracks]
    # # MyAnnotator.
    # MyAnnotator.draw_all_boxes(parsed_res)
    # MyAnnotator.dra

    # print(tracks)
    if cur > max_frames:
        break
    cv2.waitKey(1)

centers = tracker.drop_bad_tracks(min_frames=max_frames // 10)
pad = 20
# print(centers)
with_points = copy.deepcopy(first_img)
for center in centers:
    cnt, center_x, center_y = center
    # center_x = int()
    # print(center)
    heatmap[center_y - pad:center_y + pad, center_x - pad:center_x + pad] += cnt
    MyAnnotator.put_circle((center_x, center_y), with_points)
# print(centers)

# thresh = np.max(heatmap) * 4/5
# print(np.max(heatmap))
cluster_points = find_clusters(heatmap, thresh_por=max_frames // 10)

# print(cluster_points)
for point in cluster_points:
    MyAnnotator.put_circle(point, first_img)
cv2.imwrite('with_points.png', first_img)
cv2.imwrite('with_centers.png', with_points)

# print(time.time() - t)
