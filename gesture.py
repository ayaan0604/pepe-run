import cv2
import mediapipe as mp
import time

def drawSkeleton(frame, hand):
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
        cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)

    return frame

def videoMode():

        

    model_path = "hand_landmarker.task"

    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode


    # Create a hand landmarker instance with the video mode:
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path= model_path),
        running_mode=VisionRunningMode.VIDEO,
        num_hands = 4,
        min_hand_detection_confidence = 0.7,
        min_hand_presence_confidence = 0.5,
        )
    with HandLandmarker.create_from_options(options) as landmarker:
    # The landmarker is initialized. Use it here.
    
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 24)

        # Load the frame rate of the video using OpenCV’s CV_CAP_PROP_FPS
        # You’ll need it to calculate the timestamp for each frame.

        startTime = time.time()


        # Loop through each frame in the video using VideoCapture#read()

        while cap.isOpened():
            
            

            res, frame = cap.read()

            if not res:
                continue
            
            timestamp_ms = int( (time.time() - startTime) * 100)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        
            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            
                

            for hand in result.hand_landmarks:
                frame = drawSkeleton(frame, hand)
                

                    

            cv2.imshow("Hands", cv2.flip(frame,1))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()    


class GestureDetector:
    def __init__(self):
        pass