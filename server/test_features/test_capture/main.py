import threading
import queue
import time

import cv2


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
            self.q.put(frame)

    def read(self):
        """
        Возвращает самый последний кадр, считанный на данный момент, из потока.
        """
        img0 = self.q.get()
        return img0


t = time.time()
# cap = MyVideoCapture('https://s2.moidom-stream.ru/s/public/0000010493.m3u8')
print(time.time() - t)
while True:
    time.sleep(1)
t = time.time()
img = cap.read()
print(time.time() - t)
