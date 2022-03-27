from server.api.upd_api import router
from server.detection_module import DetectionModel


from fastapi import FastAPI

# dm = DetectionModel(device='cpu')

app = FastAPI()
app.include_router(router, tags=['cars_api'])

