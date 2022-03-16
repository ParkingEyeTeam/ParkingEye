from cv2 import log
import numpy as np
from PIL import Image
from sahi.predict import get_prediction
from typing import List
from pydantic import BaseModel
from sahi.prediction import PredictionResult
from sahi.utils.yolov5 import (
    download_yolov5s6_model,
)
from sahi.model import Yolov5DetectionModel


class ParsedResult(BaseModel):
    bbox: List[float]
    confidence: float
    category_id: int
    category_name: str
 
class DetectionModel:
    def __init__(self, confidence=0.3, inference_size=1920, device='cuda:0'):
        yolov5_model_path = 'models/yolov5s6.pt'
        download_yolov5s6_model(destination_path=yolov5_model_path)
        self.model = Yolov5DetectionModel(
            model_path=yolov5_model_path,
            confidence_threshold=confidence,
            device=device,  # or 'cuda:0'
        )
        self.inference_size = inference_size
 
    def predict(self, image: np.ndarray):
        image = Image.fromarray(image)
        result = get_prediction(image, self.model, image_size=self.inference_size)
        return result
 
    @staticmethod
    def parse_result(result: PredictionResult) -> List[ParsedResult]:
        lst = []
        for res in result.object_prediction_list:
            # print(res.score)
            lst.append(
                ParsedResult(bbox=res.bbox.to_voc_bbox(),
                             confidence=res.score.value,
                             category_id=res.category.id,
                             category_name=res.category.name)
            )
        return lst
 
 
# dm = DetectionModel()
# img = cv2.imread(
#     '../api/cars_test.png')
# print(DetectionModel.parse_result(dm.predict(img)))