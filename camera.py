import cv2
import time
from ultralytics import YOLO


class Camera:
    def __init__(self, model_path, cam_index=0, interval=0.1):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(cam_index)

        self.interval = interval
        self.last_infer_time = 0

        self.last_annotated_frame = None

    def dont_get_stuck():
        cv2.waitKey(1)

    def read(self):
        ret, frame = self.cap.read()
        
        if not ret:
            return None

        

        current_time = time.time()
        analyzed = False
        labels = []
        annotated_frame = None

        
        
        if current_time - self.last_infer_time >= self.interval:
            results = self.model(frame, verbose=False)

            annotated_frame = results[0].plot()
            self.last_annotated_frame = annotated_frame

            for box in results[0].boxes:
                cls = int(box.cls[0])
                labels.append(self.model.names[cls])

            labels = list(set(labels))  # remove duplicates
            self.last_infer_time = current_time
            analyzed = True

        
        


        
        
        return {
            "frame": frame,
            "annotated_frame": self.last_annotated_frame,
            "labels": labels,
            "analyzed": analyzed
        }

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)