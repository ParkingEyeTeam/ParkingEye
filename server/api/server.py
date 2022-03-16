# from fastapi import FastAPI
# import torch

# model = torch.hub.load('ultralytics/yolov5', 'custom', path='static/best.pt', force_reload=True)

# # imgs = ['https://ultralytics.com/images/zidane.jpg']  # batch of images


# app = FastAPI()

# @app.get("/")
# async def root():
#     # results = model(imgs)
#     # results.print()
#     return {"message": "Hello World"}

import torch
import server.detection_module

# dm = server.detection_module.DetectionModel()

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.