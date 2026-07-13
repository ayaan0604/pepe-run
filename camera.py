import cv2
import time
from ultralytics import YOLO
from pygrabber.dshow_graph import FilterGraph
from vision_model import gesture


def getCameraList():

    graph = FilterGraph()
    devices = graph.get_input_devices()

    return devices


class Camera:
    def __init__(self, model_path, cam_index=0, interval=0.3):
        self.model = gesture.GestureDetector()
        self.camIndex = cam_index
        self.cap = None
        self.enabled = True
        self.interval = interval
        self.last_infer_time = 0


        self.cameraList = getCameraList()

        self.last_detected_hand = None
        self.last_detection_time = 0

    def dont_get_stuck():
        cv2.waitKey(1)

    def setCamIndex(self, camName):
        try:
            self.camIndex = self.cameraList.index(camName)
        except ValueError:
            print("Camera not found in list:", camName)


    def startCam(self ):
        try:
            self.cap = cv2.VideoCapture(self.camIndex)
            
        except:
            print("Cant open camera")
            print(self.camIndex)

    def read(self):
        try:
            ret, frame = self.cap.read()
        except:
            print('Cant operate Camera')
            return None, None
        
        
        if not ret:
            return None, None

        

        current_time = time.time()
        labels = []

        
        

        if current_time - self.last_infer_time >= self.interval:

            result = self.model.get_landmarks(frame)
            for hand in result.hand_landmarks:
                labels = self.model.get_labels(hand)
                self.last_detected_hand = hand
                self.last_detection_time = current_time
        
        time_since_last_detection = current_time - self.last_detection_time

        if (self.last_detected_hand is not None) and time_since_last_detection <0.1:
            return self.model.draw_skeleton(self.last_detected_hand,frame), labels

        return frame, labels
        
       
        for hand in result.hand_landmarks:
            labels = self.model.get_labels(hand)
            annotated_frame = self.model.draw_skeleton(hand, frame)
        return annotated_frame, labels
        self.last_annotated_frame = annotated_frame
        
                    
        self.last_infer_time = current_time
            


        return {
            "frame": frame,
            "annotated_frame": self.last_annotated_frame,
            "labels": labels,
            "analyzed": analyzed
        }

    def release(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)


if __name__ == "__main__":
   pass