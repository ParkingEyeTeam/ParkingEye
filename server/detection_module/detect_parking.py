import copy
import time

import cv2
import numpy as np

from detection_model import DetectionModel
from my_tracker import Tracker
from drawing import MyAnnotator


class ParkingPlacesFinder:
    def __init__(self, video_dir='C:\\Users\\igors\\Videos\\test_3.mp4', inference_size=1920, frame_skip=5):
        self.model = DetectionModel(inference_size=inference_size)
        self.tracker = Tracker()
        self.video_dir = video_dir
        self.max_frames = 1000
        self.frame_skip = 5

    def main_loop(self):
        t = time.time()
        cap = cv2.VideoCapture(self.video_dir)
        cur = 0
        heatmap = None
        max_frames = 1000
        first_img = None
        while cap.isOpened():
            ret, frame = cap.read()
            if first_img is None:
                first_img = copy.deepcopy(frame)
                heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=int)
            if not ret:
                break
            cur += 1
            if cur % self.frame_skip != 0:
                continue
            result = self.model.predict(frame)
            parsed_res = DetectionModel.parse_result(result)
            dets = [pred.bbox for pred in parsed_res]

            np_dets = np.array(dets)

            tracks = self.tracker.track(np_dets)
            tracks = [list(map(int, track)) for track in tracks]
            for track in tracks:
                start = (track[0], track[1])
                end = (track[2], track[3])
                _id = str(track[4])
                MyAnnotator.rectangle(frame, start, end)
                MyAnnotator.put_text(frame, _id, (start[0], start[1]))
            cv2.imshow('test', frame)

            if cur > max_frames:
                break
            cv2.waitKey(1)

        centers = self.tracker.drop_bad_tracks(min_frames=max_frames // 10)
        pad = 10
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
        cluster_points = ParkingPlacesFinder.find_clusters(heatmap, thresh_por=max_frames // 10)

        print(cluster_points)
        for point in cluster_points:
            MyAnnotator.put_circle(point, first_img)
        cv2.imwrite('with_points.png', first_img)
        cv2.imwrite('with_centers.png', with_points)

    @staticmethod
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

finder = ParkingPlacesFinder('C:\\Users\\igors\\Videos\\test_2.mp4')
finder.main_loop()