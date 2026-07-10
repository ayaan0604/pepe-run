import os
import cv2
import mediapipe as mp
import pandas as pd
import tqdm

def getVideoFiles(folder):
    
    return [file for file in os.listdir(folder) if os.path.isfile( os.path.join(folder, file) )]

def extractFrames(videoPath, frameCount):

    cap = cv2.VideoCapture(videoPath)

    frameNumber = 0
    extractedFrames = []

    while cap.isOpened():

        res, frame = cap.read()

        if not res:
            break

        if frameNumber % frameCount == 0 :
            extractedFrames.append(frame)
        
        frameNumber+=1
    
    cap.release()
    return extractedFrames

def creatModel():
    model_path = "../hand_landmarker.task"

    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode


    # Create a hand landmarker instance with the video mode:
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path= model_path),
        running_mode=VisionRunningMode.IMAGE,
        num_hands = 2,
        min_hand_detection_confidence = 0.7,
        min_hand_presence_confidence = 0.5
        )

    return HandLandmarker.create_from_options(options)

def getMediaPipeResult(model, frame):
    
    

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame received from OpenCV to a MediaPipe’s Image object.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)


    return model.detect(mp_image)

def getData(result):

    hands = result.hand_landmarks
    data = []

    for i, hand in enumerate(hands):
        hand_data= {}
        hand_data['hand'] = result.handedness[i][0].category_name
        hand_data['confidence'] = result.handedness[i][0].score

        wrist = hand[0]

        #normalise with respect to wrist and save
        
        for idx ,lm in enumerate(hand):
            
            hand_data[f"x{idx}"] = lm.x - wrist.x
            hand_data[f"y{idx}"] = lm.y - wrist.y
            hand_data[f"z{idx}"] = lm.z - wrist.z
        data.append(hand_data)
    
    return data
        
        
def extract_data_to_csv():
    folderNames = ['up', 'left', 'down', 'right', 'none']
    model = creatModel()

    final_data = []
    id = 0
    totalCount = 0
    for folder in folderNames:
        
        videoNames = getVideoFiles(folder)
        
        
        for video in videoNames:
            print(f"Analysing {folder}: {video}")
            frames = extractFrames(os.path.join(folder, video), 3) 
            for frame in tqdm.tqdm(frames):

                result = getMediaPipeResult(model, frame)
                if not result.hand_landmarks:
                    continue

                data = getData(result)
                for handData in data:

                    handData['video'] = video
                    handData['id'] = id
                    id+=1

                    handData['label'] = folder

                    final_data.append(handData)

                

    print("total rows extracted: ", len(final_data))

    df = pd.DataFrame(final_data)
    df.to_csv("gesture_classification_dataset.csv")
    print("data Successfully written to csv")

    

    

    
    
    

    
    
        
    

if __name__ == "__main__":
    df = pd.read_csv("gesture_classification_dataset.csv")

    print(df.shape)

    print(df.columns)

    print(df.isna().sum())

    print(df["label"].value_counts())

    print(df["hand"].value_counts())