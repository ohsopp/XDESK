from gpiozero import AngularServo, Motor, PWMOutputDevice, DistanceSensor
import socket
import time
import sys

# 리니어 액추에이터 설정
enA = PWMOutputDevice(18) # PWM 신호 제어
in1 = 23
in2 = 24
motorA = Motor(forward=in1, backward=in2)

# 서보 모터 설정
servo = AngularServo(16, min_angle=0, max_angle=90)
servo_reset = 55
servo_up = 45
servo_down = 75

# 모션 데스크 버튼 활성화 (한 번 눌러줘야 활성화 됨)
servo.angle = servo_down
time.sleep(0.3)
servo.angle = servo_reset
time.sleep(0.3)

# 초음파 센서 설정
sensor_desk = DistanceSensor(echo=6, trigger=5)
sensor_laptop = DistanceSensor(echo=27, trigger=17)

# 클라이언트 설정
HOST = '192.168.137.196' # 서버의 IP 주소 (젯슨 오린 나노)
PORT = 13245  # 서버와 같은 포트 번호 사용

# 인자로 포트 받기 (0에서 65535 사이 랜덤 정수)
# 포트가 해제되기 전에 같은 포트를 다시 할당하는 것을 방지
if len(sys.argv) == 2:
    PORT = int(sys.argv[1]) # 인자로 받은 포트 번호 사용
    print(f"PORT: {PORT}")

# 모드 설정 
modes = ['ready', 'servo', 'linear', 'stop']
mode_num = 0

# 서보 모터 작동
def servo_motor(data):
    global servo
    if data.lower() == 'up': # 책상을 위로 이동
        servo.angle = servo_up
        time.sleep(0.3)
    elif data.lower() == 'down': # 책상을 아래로 이동
        servo.angle = servo_down
        time.sleep(0.3)
    else: # 책상 정지
        servo.angle = servo_reset
        time.sleep(0.3)

# 리니어 액추에이터 작동
def linear_motor(data, speed):
    global enA
    if data.lower() == 'up': # 노트북 거치대 위로 이동
        motorA.forward()
    elif data.lower() == 'down': # 노트북 거치대 아래로 이동
        motorA.backward()
    else: # 노트북 거치대 정지
        motorA.stop()
    # PWM 듀티 사이클을 설정
    enA.value = speed / 100.0

# TCP/IP 소켓 통신 (클라이언트)
def socket_client():
    global mode_num, servo
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = s.recv(1024)
            data = data.decode()
            
            # 연결 성공
            if data == 'Welcome!':
                print(data)
                mode_num = 1 # 서보 모터 모드
                while True:
                    try:
                        data = s.recv(1024)
                        if not data:
                            continue
                        
                        # 서버에서 보낸 데이터
                        data = data.decode()
                        #print(f"Received from server: {data}")
                        
                        # 서보 모터에서 리니어액추에이터로 변경 (책상에서 거치대로)
                        if data == 'switch':
                            mode_num = 2 # 리니어액추에이터 모드
                            servo.angle = servo_reset
                            time.sleep(0.3)
                        # 모든 작업을 멈추고 종료 준비
                        elif data == 'stop':
                            mode_num = 3 # 정지 모드
                            motorA.stop()
                        # 종료
                        elif data == 'exit':
                            # 책상과 거치대 높이 반환
                            print(round(sensor_desk.distance * 100), round(sensor_laptop.distance * 100))
                            break
        
                        if modes[mode_num] == modes[1]:
                            servo_motor(data)
                        elif modes[mode_num] == modes[2]:
                            linear_motor(data, 100)
                    except socket.timeout:
                        print("Socket timed out. Exiting.")
                        break
            # 연결 실패
            else:
                print(f"Rejected connection from server.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        try:
            # 모든 장치 닫기 및 리소스 해제 (필수)
            servo.close()
            enA.close()
            motorA.close()
            sensor_desk.close()
            sensor_laptop.close()
            print("Resources have been released.")
        except Exception as ex:
            print(f"Error while closing GPIO resources: {ex}")


if __name__ == '__main__':
    socket_client()
    