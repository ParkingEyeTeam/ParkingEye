import numpy as np
from PIL import Image
from sahi.predict import get_prediction, get_sliced_prediction
from typing import List
from pydantic import BaseModel
from sahi.prediction import PredictionResult
import os
from sahi.utils.yolov5 import (
    download_yolov5s6_model,
)
from sahi.model import Yolov5DetectionModel


class ParsedResult(BaseModel):
    bbox: List[int]
    confidence: float
    category_id: int
    category_name: str


class DetectionModel:
    def __init__(self, confidence=0.3, inference_size=1920, device='cuda:0', det_type='usual'):
        yolov5_model_path = os.path.dirname(os.path.realpath(__file__)) + '/models/yolov5s6.pt'
        download_yolov5s6_model(destination_path=yolov5_model_path)
        self.det_type = det_type
        self.model = Yolov5DetectionModel(
            model_path=yolov5_model_path,
            confidence_threshold=confidence,
            device=device,  # or 'cuda:0'
        )

        self.inference_size = inference_size

    def predict(self, image: np.ndarray):
        image = Image.fromarray(image)
        if self.det_type == 'sliced':
            result = get_sliced_prediction(
                image,
                self.model,
                slice_height=400,
                slice_width=400,
                overlap_height_ratio=0.2,
                overlap_width_ratio=0.2
            )
        else:
            result = get_prediction(image, self.model, image_size=self.inference_size)
        return result

    @staticmethod
    def parse_result(result: PredictionResult) -> List[ParsedResult]:
        lst = []
        for res in result.object_prediction_list:
            if res.category.name in ['car']:
                lst.append(
                    ParsedResult(
                        bbox=list(map(int, res.bbox.to_voc_bbox())),
                        confidence=res.score.value,
                        category_id=res.category.id,
                        category_name=res.category.name)
                )
        return lst
