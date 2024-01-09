import cv2 as cv
import torch
import numpy as np

model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt')

class Video(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv.flip(frame, 1)

        results = model(frame)
        print(results)
        result_frame = np.squeeze(results.render())

        ret, jpg = cv.imencode('.jpg', result_frame)
        return jpg.tobytes()