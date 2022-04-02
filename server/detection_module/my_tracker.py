from sort import Sort
import numpy as np
from typing import Dict, List


class Tracker:
    def __init__(self):
        self.sort = Sort()
        self.tracked_objects: Dict[int, List] = {}

    def track(self, detections: np.ndarray):
        """
        Обновляет актуальный треки.
        """
        if len(detections) == 0:
            return []

        tracked_dets = self.sort.update(detections)
        for cur_track in tracked_dets:
            self.add_track(cur_track)

        return tracked_dets

    def add_track(self, cur_track):
        x0, y0, x1, y1, _id = cur_track
        if _id not in self.tracked_objects.keys():
            self.tracked_objects[_id] = [(x0, y0, x1, y1)]
        else:
            self.tracked_objects[_id].append((x0, y0, x1, y1))

    def drop_bad_tracks(self, possible_dif=100, min_frames=300):
        def get_center(bbox):
            return bbox[0] + (bbox[2] - bbox[0]) // 2, bbox[1] + (bbox[3] - bbox[1]) // 2

        def first_call(point, dif):
            def second_call(in_point):
                if (point[0] - in_point[0]) ** 2 + (point[1] - in_point[1]) ** 2 <= dif ** 2:
                    return 1
                return 0

            return second_call

        ret_centers = None
        for _id in self.tracked_objects.keys():
            x_pos, y_pos = 0, 0
            # for box in self.tracked_objects[_id]:
            if len(self.tracked_objects[_id]) < min_frames:
                # print(1)
                continue
            np_ar = np.array(self.tracked_objects[_id])
            centers = np.apply_along_axis(get_center, 1, np_ar)
            center_new = np.mean(centers, axis=0)
            min_point = np.min(centers, axis=0)
            max_point = np.max(centers, axis=0)
            # mask = np.apply_along_axis(first_call(center_new, possible_dif / 2), 1, centers)
            if (center_new[0] - min_point[0]) ** 2 + (center_new[1] - min_point[1]) ** 2 <= \
                    (possible_dif / 2) ** 2 and \
                    (center_new[0] - max_point[0]) ** 2 + (center_new[1] - max_point[1]) ** 2 <= \
                    (possible_dif / 2) ** 2:
                # print(_id)
                if ret_centers is None:
                    # ret_centers = np.array(centers)
                    ret_centers = [[len(centers), int(center_new[0]), int(center_new[1])]]
                else:
                    # ret_centers = np.concatenate((ret_centers, centers), axis=0)
                    ret_centers += [[len(centers), int(center_new[0]), int(center_new[1])]]
        # print(_id)
        return ret_centers
