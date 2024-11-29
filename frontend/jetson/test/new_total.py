# 임베디드 최적화 코드 (해상도 50% 버전)
import cv2
import mediapipe as mp
import numpy as np
import time
import socket
import multiprocessing
from multiprocessing import Process, Pipe, Value
import sys
import os

mp_pose = mp.solutions.pose

# 비디오 캡처 초기화 함수
def get_video_device_number():
    video_devices = [int(f[-1]) for f in os.listdir('/dev') if f.startswith('video')]
    if not video_devices:
        print("No video devices found.")
        exit()
    return min(video_devices)

# 비디오 캡처 초기화
video_device_number = get_video_device_number()  # 첫 번째 비디오 장치 번호 가져오기
#print(video_device_number)
cap = cv2.VideoCapture(video_device_number)
previous_time = 0

# 해상도 축소 비율 (2로 나누어 해상도를 절반으로 줄임)
resize_factor = 2

# 서버 설정
HOST = '0.0.0.0'  # 모든 IP 주소에서 연결 허용
PORT = 13245  # 클라이언트와 동일한 포트 번호

# 인자로 PORT 받기
if len(sys.argv) == 2:
    PORT = int(sys.argv[1])  # 인자로 받은 포트 번호 사용
    print(f"PORT: {PORT}")

# 허용된 클라이언트 IP 주소 목록
ALLOWED_CLIENT_IPS = ['192.168.137.194', '192.168.137.50']  # 허용된 클라이언트의 IP 주소

# 자동 모드 옵션
modes = ['ready', 'servo', 'linear', 'stop']
mode_num = Value('i', 0)

# 책상 높이, 거치대 높이
desk_height = 0
laptop_height = 0

direction = 0

def socket_server(conn_pipe):
    global desk_height, laptop_height
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        # 서버 소켓을 수신 대기 상태로 설정
        s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()

        # 클라이언트 IP 주소가 허용된 목록에 있는지 확인
        client_ip = addr[0]
        if client_ip in ALLOWED_CLIENT_IPS:
            print(f"Accepted connection from {client_ip}")
            conn.send(b'Welcome!')
            can_conn = True
            mode_num.value = 1
            print('start')
        else:
            print(f"Rejected connection from {client_ip}")
            conn.close()
            can_conn = False
            conn = None

        while can_conn:
            if conn_pipe.poll():
                message = conn_pipe.recv()
                conn.sendall(message.encode())
                print(message)
                
                if message == 'exit':
                    break


def move_desk(conn_pipe, landmarks, h, w):
    global direction

    diff = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h - landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * h
    #print(diff)
    
    if diff < 45:
        if direction != 0 and direction == 1:
            time.sleep(0.3)
            direction = 2
        conn_pipe.send('down')
    elif diff > 50:
        if direction != 0 and direction == 2:
            time.sleep(0.3)
            direction = 1
        conn_pipe.send('up')
    else:
        conn_pipe.send('switch')
        mode_num.value = 2
    

def move_laptop(conn_pipe, landmarks, h):
    third_top = h / 3 * 1 - 5
    third_bottom = h / 3 * 1 + 5

    # 눈 좌표 추출
    left_eye_y = landmarks[mp_pose.PoseLandmark.LEFT_EYE].y * h
    right_eye_y = landmarks[mp_pose.PoseLandmark.RIGHT_EYE].y * h
    eyes_y = (left_eye_y + right_eye_y) / 2
    
    #print(left_eye_y, right_eye_y, eyes_y)
    #print(third_top, third_bottom)
    
    # 눈이 화면 아래에 위치
    if eyes_y > third_bottom:
        conn_pipe.send('down')
    # 눈이 화면 위에 위치
    elif eyes_y < third_top:
        conn_pipe.send('up')
    # 눈이 화면 중앙에 위치
    else:
        conn_pipe.send('stop')
        mode_num.value = 3

def camera_processing(conn_pipe):
    global cap, previous_time
    
    try:
        with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
    
                image = cv2.flip(image, 1)
    
                # 이미지 해상도 축소
                h, w, _ = image.shape
                image = cv2.resize(image, (w // resize_factor, h // resize_factor))
                #print(h, w, image.shape[0], image.shape[1])
    
                # 흰색 배경 이미지 생성
                white_background = np.ones((image.shape[0], image.shape[1], 3), dtype=np.uint8) * 255
      
                # 이미지 처리
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)
    
                # 현재 시간
                current_time = time.time()
    
                # 키포인트 및 연결선 그리기
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
    
                    # 각 랜드마크 그리기
                    for landmark in landmarks:
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        cv2.circle(white_background, (x, y), 5, (0, 0, 255), -1)

                    # 랜드마크 연결선 그리기
                    for connection in mp_pose.POSE_CONNECTIONS:
                        start_idx, end_idx = connection
                        start_point = (int(landmarks[start_idx].x * w), int(landmarks[start_idx].y * h))
                        end_point = (int(landmarks[end_idx].x * w), int(landmarks[end_idx].y * h))
                        cv2.line(white_background, start_point, end_point, (0, 255, 0), 2)

                    # 오른팔 각도 or 눈 높이 계산 및 모터 제어 (0.5초마다)
                    if current_time - previous_time >= 0.5:
                        if modes[mode_num.value] == modes[1]:
                            move_desk(conn_pipe, landmarks, image.shape[0], image.shape[1])
                        if modes[mode_num.value] == modes[2]:
                            move_laptop(conn_pipe, landmarks, image.shape[0])
                        elif modes[mode_num.value] == modes[3]:
                            conn_pipe.send('exit')
                            break
                        previous_time = current_time
    
                #cv2.imshow('Keypoints with Connections on White Background', white_background)
                #if cv2.waitKey(5) & 0xFF == 27: break

    except Exception as e:
        print(f"An error occurred during camera processing: {e}")
        
    finally:
        cap.release()
        #cv2.destroyAllWindows()
        print("Camera released.")

if __name__ == '__main__':
    print(f"Number of CPU cores: {multiprocessing.cpu_count()}")

    # 파이프 생성
    socket_conn, camera_conn = Pipe()

    # 프로세스 생성
    socket_process = Process(target=socket_server, args=(socket_conn,))
    camera_process = Process(target=camera_processing, args=(camera_conn,))

    # 프로세스 시작
    socket_process.start()
    camera_process.start()

    # 프로세스가 종료될 때까지 대기
    camera_process.join()
    socket_conn.send('exit')
    socket_process.join()
