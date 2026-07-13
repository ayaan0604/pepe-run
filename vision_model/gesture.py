## the goal of this file is to make a pipeline that takes up raw opencv captured image and gives out
## skeleton drawn on the image, the gesture label
import torch
import cv2
import mediapipe as mp
import time
import pandas as pd
import pickle as pkl




class GestureClassifierNetwork(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.network = torch.nn.Sequential(
            torch.nn.Linear(63, 64),
            torch.nn.ReLU(),

            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),

            torch.nn.Linear(32, 5)
        )

    def forward(self, x):
        return self.network(x)

class GestureClassifier:
    def __init__(self, path):
        self.model = self.get_model(path)

    def get_model(self,path):
        pass


class GestureDetector:
    def __init__(self):
        
        self.landmarker_model = self.get_landmarker_model("vision_model/hand_landmarker.task")

        self.gesture_classifier = self.get_gesture_model("vision_model/ver1/state_dict.pth")

        self.labelEncoder = self.get_label_encoder("vision_model/ver1/LabelEncoder.pkl")

        self.startTime = time.time()


    def get_gesture_model(self, path):

        if __name__ == "__main__":
            path = 'ver1/state_dict.pth'

        model = GestureClassifierNetwork()
        model.load_state_dict(torch.load(path, weights_only=True))
        model.eval()

        return model
    
    def get_label_encoder(self, path):
        if __name__ == "__main__":
            path = 'ver1/LabelEncoder.pkl'

        with open(path, 'rb') as f:
            return pkl.load(f)

    def get_labels(self, hand):
        
        ##data extraction
        wrist = hand[0]

        hand_data = {}
        for idx ,lm in enumerate(hand):
            
            hand_data[f"x{idx}"] = lm.x - wrist.x
            hand_data[f"y{idx}"] = lm.y - wrist.y
            hand_data[f"z{idx}"] = lm.z - wrist.z

        #transformation
        dataframe = pd.DataFrame([hand_data])

        input_tensor = torch.tensor(dataframe.values, dtype= torch.float32)

        #output
        with torch.no_grad():
            output_label = self.gesture_classifier(input_tensor).argmax(dim=1).cpu().numpy()
        
        return self.labelEncoder.inverse_transform(output_label)

        
        
        

    def get_landmarker_model(self, path):
        
        if __name__ == "__main__":
            path = 'hand_landmarker.task'

        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode


        # Create a hand landmarker instance with the video mode:
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path= path),
            running_mode=VisionRunningMode.VIDEO,
            num_hands = 1,
            min_hand_detection_confidence = 0.7,
            min_hand_presence_confidence = 0.5
            )
        
        return HandLandmarker.create_from_options(options)

    def get_landmarks(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame received from OpenCV to a MediaPipe’s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        timestamp_ms = int( (time.time() - self.startTime) * 100)

        return self.landmarker_model.detect_for_video(mp_image, timestamp_ms)
    
    def draw_skeleton(self,hand, frame):

        HAND_CONNECTIONS = [
            (0,1), (1,2), (2,3), (3,4),          # Thumb
            (0,5), (5,6), (6,7), (7,8),          # Index
            (5,9), (9,10), (10,11), (11,12),     # Middle
            (9,13), (13,14), (14,15), (15,16),   # Ring
            (13,17), (17,18), (18,19), (19,20),  # Pinky
            (0,17)                               # Palm
        ]

        #drawing points
        h, w = frame.shape[:2]

        # Draw bones
        for start, end in HAND_CONNECTIONS:
            p1 = hand[start]
            p2 = hand[end]

            x1, y1 = int(p1.x * w), int(p1.y * h)
            x2, y2 = int(p2.x * w), int(p2.y * h)

            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw joints
        for lm in hand:
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (x, y), 4, (0, 255, 255), -1)

        return frame
    
    

        
        

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    model = GestureDetector()

    while cap.isOpened():

        res, frame = cap.read()

        if not res:
            continue

        result = model.get_landmarks(frame)

        if result is not None:
            for hand in result.hand_landmarks:
                label = model.get_labels(hand)
                frame = model.draw_skeleton(hand, frame)

                text = label[0]
                position = (50, 100)      # (X, Y) coordinates of the bottom-left corner of the text
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1            # Font size multiplier
                color = (0, 255, 0)       # Text color in BGR format (this is green)
                thickness = 2             # Thickness of the stroke

                
                cv2.putText(frame, text, position, font, font_scale, color, thickness)


        
        cv2.imshow("test", frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()    



        

