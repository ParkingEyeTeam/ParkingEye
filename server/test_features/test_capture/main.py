import threading
import queue
import time

import cv2
import sys


class MyAnnotator:
    @staticmethod
    def put_text(frame, text, position, scale=1, color=(0, 0, 255), thickness=2):
        """
        Добавляет текст на изображение
        """
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_COMPLEX, scale, color, thickness)

    @staticmethod
    def rectangle(frame, start, end, color=(0, 0, 255), thickness=2):
        """
        Рисует квадрат на изображении
        """
        cv2.rectangle(frame, start, end, color, thickness)


class MyVideoCapture:
    """
    Класс для считывания потока.
    Реализует асинхронную очередь для выдачи только последннего считанного кадра.
    """

    def __init__(self, name, img_size=640, stride=32):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        self.name = name
        t = threading.Thread(target=self._reader)
        t.daemon = True
        self.img_size = img_size
        self.stride = stride
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        bad_cnt = 0
        thresh = 60
        while True:
            if thresh < bad_cnt:
                print('Не могу получить кадры со стрима: ', self.name)
                exit(1)
            ret, frame = self.cap.read()
            if not ret:
                self.cap.open(self.name)
                bad_cnt += 1
                continue
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            bad_cnt = 0
            # cv2.waitKey(1)
            time.sleep(0.025)
            self.q.put(frame)

    def read(self):
        """
        Возвращает самый последний кадр, считанный на данный момент, из потока.
        """
        img0 = self.q.get()
        return img0


import cv2
import threading


# bufferless VideoCapture
class MyVideoCapture2:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    # grab frames as soon as they are available
    def _reader(self):
        while True:
            ret = self.cap.grab()
            if not ret:
                break

    # retrieve latest frame
    def read(self):
        ret, frame = self.cap.retrieve()
        return frame


t = time.time()
cap = MyVideoCapture('https://s2.moidom-stream.ru/s/public/0000010493.m3u8')
# cap = cv2.VideoCapture('https://s2.moidom-stream.ru/s/public/0000010493.m3u8')
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
# cap = cv2.VideoCapture(0)
# cap = MyVideoCapture(0)
print(time.time() - t)

while True:
    frame = cap.read()
    # if not ret:
    #     pass
    # else:
    cv2.imshow('123', frame)
    cv2.waitKey(50)
    # time.sleep(1)
t = time.time()
img = cap.read()
print(time.time() - t)
