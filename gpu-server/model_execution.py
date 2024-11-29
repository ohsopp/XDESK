import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Add, Input, Embedding, GlobalAveragePooling1D, Conv1D, ReLU, MaxPooling1D, LSTM, Dense, Bidirectional, Dropout, BatchNormalization

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities


def mediapipe_detection(image, model): 
    #image = feed frame
    #model = Holistic model
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR -> RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB -> BGR
    return image, results


#connection_drawing_spec 커스텀 (optional)
def draw_styled_landmarks(image, results):
    #Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             ) 
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             ) 


def extract_keypoints_258(results):
    # result의 landmarks의 모든 key point values -> 하나의 numpy array 로 flatten
    #if landmarks has no value, fill numpy array with zero
    
    if results.pose_landmarks: #pose landmarks
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() 
    else:
        pose = np.zeros(132) #33*4

    if results.left_hand_landmarks: #left hand landmarks
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() 
    else:
        lh = np.zeros(63) #21*3

    if results.right_hand_landmarks: #right hand landmarks
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() 
    else:
        rh = np.zeros(63) #21*3
    
    return np.concatenate([pose, lh, rh])

mode = 1


#num of videos
no_sequences = 60

if mode == 1:
    actions123 = np.array(['가슴', '개', '귀', '내일', '누나', '다리', '동생', '뒤', '딸', '머리', '목', '물', '발', '배', '불', '뼈', '선생님', '손', '아기', '아내', '아들', '아빠', '앞', '어제', '엄마', '옆쪽', '오늘', '오른쪽', '왼쪽', '위', '친구', '코', '팔', '학교', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    actions456 = np.array(['chest', 'dog', 'ear', 'tomorrow', 'sister', 'leg', 'sister2', 'back', 'daughter', 'head', 'neck', 'water', 'foot', 'stomach', 'fire', 'bone', 'teacher', 'hand', 'baby', 'wife', 'son', 'dad', 'front', 'yesterday', 'mom', 'side', 'today', 'right', 'left', 'up', 'friend', 'nose', 'arm', 'school', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero'])
    actions = np.array(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43'])
elif mode == 2:
    actions = np.array(['볼하트', '걸어다닙니다', '고양이', '최고', '손흥민'])

# 1 Video = 50 frames
sequence_length = 30


#Residual Block 구현
def residual_block(x, filters, kernel_size=3, stride=1):
    # Shortcut Connection
    shortcut = x
    
    # Main Path
    x = Conv1D(filters, kernel_size=kernel_size, strides=stride, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    
    x = Conv1D(filters, kernel_size=kernel_size, strides=stride, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    
    x = Conv1D(filters, kernel_size=kernel_size, strides=stride, padding='same')(x)
    x = BatchNormalization()(x)
    
    # Shortcut Connection 추가
    x = Add()([x, shortcut])
    x = ReLU()(x)
    
    return x


input_layer = Input(shape=(30,258))

x = Conv1D(64, kernel_size=3, activation='relu')(input_layer)
x = BatchNormalization()(x)
x = ReLU()(x)
x = MaxPooling1D(pool_size=2)(x)

# --------------------------------------------------------
x = residual_block(x, filters=64)
x = MaxPooling1D(pool_size=2, padding='same')(x)

x = residual_block(x, filters=64)
x = MaxPooling1D(pool_size=2, padding='same')(x)

x = residual_block(x, filters=64)
x = MaxPooling1D(pool_size=2)(x)

# --------------------------------------------------------

x = Bidirectional(LSTM(64, return_sequences=True, activation='tanh'))(x)
x = Dropout(0.3)(x)
x = Bidirectional(LSTM(128, return_sequences=True, activation='tanh'))(x)
x = Dropout(0.3)(x)
x = Bidirectional(LSTM(64, return_sequences=True, activation='tanh'))(x)
x = Dropout(0.3)(x)
x = Bidirectional(LSTM(64, return_sequences=True, activation='tanh'))(x)
x = Dropout(0.3)(x)
x = LSTM(64, return_sequences=False, activation='relu')(x)


output_layer = Dense(actions.shape[0], activation='softmax')(x)
model = Model(inputs=input_layer, outputs=output_layer)
#model.summary()


# In[15]:
if mode == 1:
    model.load_weights('model_44_258.h5')
elif mode == 2:
    model.load_weights('ssafy_model_258(2).h5')


inf_res = '100'

# prediction using video
def custom_video_prediction(video):
    global inf_res
    inf_res = 'none'
    
    # 1. detection variables
    sequence = [] #collect 60 frames to make a sequence(=video)
    threshold = 0.995
    word = ''
    cnt = 0
    frame_num = 0

    cap = cv2.VideoCapture(video)
    # Set mediapipe model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            # Read video
            ret, frame = cap.read()
            if ret == False:
                break
                
            frame_num = frame_num + 1
            if frame_num % 2 == 0:
                continue

            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            #print(results)

            # 2. Prediction logic
            keypoints = extract_keypoints_258(results)
            sequence.append(keypoints)
            sequence = sequence[-30:] #generate sequence with last 30 frames


            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions123[np.argmax(res)])
                
                if word == actions[np.argmax(res)]:
                    cnt = cnt + 1
                else :
                    word = actions[np.argmax(res)]
                    cnt = 1
                    
                #3. Rendering logic
                if res[np.argmax(res)] > threshold and cnt >= 5: 
                    inf_res = actions[np.argmax(res)]
                    print("[RESULT]", inf_res, ", index:", np.argmax(res))
                    return  inf_res
        return inf_res



#curDir = "/home/j-i11a102/jeonghyeon/saved_video"
#curDir = "/home/j-i11a102/face_recognition/face_recognition_master/saved_video"
#videoPath = "/home/j-i11a102/jeonghyeon/saved_video/motion.mp4"
#custom_video_prediction(videoPath)
#print("[RESULT]", inf_res)



#for file in os.listdir(curDir):
#    if(file.endswith(".mp4")):
#        path = os.path.join(curDir, file)
#        custom_video_prediction(path)
#        print("[RESULT]", inf_res)
def main():
    #curDir = "/home/j-i11a102/face_recognition/face_recognition_master/saved_video"
    videoPath = "/home/j-i11a102/face_recognition/face_recognition_master/saved_video/motion.mp4"
    result = custom_video_prediction(videoPath)
    return result

