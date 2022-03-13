import cv2


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
