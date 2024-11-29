from gpiozero import AngularServo, Motor, PWMOutputDevice, DistanceSensor
import socket
import time
import sys

# 리니어 액추에이터 설정
enA = PWMOutputDevice(18)
in1 = 23
in2 = 24
motorA = Motor(forward=in1, backward=in2)

# 서보 모터 설정
servo = AngularServo(16, min_angle=0, max_angle=90)
servo_reset = 55
servo_left = 45
servo_right = 75
servo.angle = servo_right
time.sleep(0.3)
servo.angle = servo_reset
time.sleep(0.3)

# 초음파 센서 설정
sensor_desk = DistanceSensor(echo=6, trigger=5)
sensor_laptop = DistanceSensor(echo=27, trigger=17)

# 클라이언트 설정
HOST = '192.168.137.157' # 서버의 IP 주소
PORT = 13245  # 서버와 같은 포트 번호 사용

# 인자로 PORT 받기
if len(sys.argv) == 2:
    PORT = int(sys.argv[1])  # 인자로 받은 포트 번호 사용
    print(f"PORT: {PORT}")


modes = ['ready', 'servo', 'linear', 'stop']
mode_num = 0

def servo_motor(data):
    global servo
    if data.lower() == 'up':
        servo.angle = servo_left
        time.sleep(0.3)
    elif data.lower() == 'down':
        servo.angle = servo_right
        time.sleep(0.3)
    else:
        servo.angle = servo_reset
        time.sleep(0.3)

def linear_motor(data, speed):
    global enA
    if data.lower() == 'up':
        motorA.forward()
    elif data.lower() == 'down':
        motorA.backward()
    enA.value = speed / 100.0

def socket_client():
    global mode_num, servo
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = s.recv(1024)
            data = data.decode()
            if data == 'Welcome!':
                print(data)
                mode_num = 1
                while True:
                    try:
                        data = s.recv(1024)
                        if not data:
                            continue
                        data = data.decode()
                        #print(f"Received from server: {data}")
        
                        if data == 'switch':
                            mode_num = 2
                            servo.angle = servo_reset
                            time.sleep(0.3)
                        elif data == 'stop':
                            mode_num = 3
                            motorA.stop()
                        elif data == 'exit':
                            print(round(sensor_desk.distance * 100), round(sensor_laptop.distance * 100))
                            break
        
                        if modes[mode_num] == modes[1]:
                            servo_motor(data)
                        elif modes[mode_num] == modes[2]:
                            linear_motor(data, 100)
        
                    except socket.timeout:
                        print("Socket timed out. Exiting.")
                        break
                    
            else:
                print(f"Rejected connection from server.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        try:
            # 모든 장치 닫기 및 리소스 해제
            servo.angle = servo_reset
            time.sleep(0.5)
            servo.close()
            
            motorA.stop()  
            enA.close()
            motorA.close()
            
            sensor_desk.close()
            sensor_laptop.close()
            
            print("Resources have been released.")
        except Exception as ex:
            print(f"Error while closing GPIO resources: {ex}")


if __name__ == '__main__':
    socket_client()
    
