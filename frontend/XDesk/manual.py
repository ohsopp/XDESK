# from gpiozero import AngularServo, Motor, PWMOutputDevice, DistanceSensor
import time
from PySide6.QtCore import QObject, Slot

class ServoMotor:
    # pass

    def __init__(self):
        self.servo_reset = 55
        self.servo_up = 45
        self.servo_down = 75

        self.in1 = 23
        self.in2 = 24

    # 핀 할당
    def initialization(self):
        # 서보 모터 설정
        self.servo = AngularServo(16, min_angle=0, max_angle=90)
        self.servo.angle = self.servo_reset

        # 리니어 액추에이터 설정
        self.enA = PWMOutputDevice(18)
        self.enA.value = 1
        self.motor = Motor(forward=self.in1, backward=self.in2)

        # 초음파 센서 설정
        self.sensor_desk = DistanceSensor(echo=6, trigger=5)
        self.sensor_laptop = DistanceSensor(echo=27, trigger=17)

    def move_servo_save(self, target_height):
        distance = round(self.sensor_desk.distance * 100)
        if distance < target_height:
            self.servo.angle = self.servo_up
            time.sleep(0.3)
            self.servo.angle = self.servo_reset
            time.sleep(0.4)
        elif distance > target_height:
            self.servo.angle = self.servo_down
            time.sleep(0.3)
            self.servo.angle = self.servo_reset
            time.sleep(0.4)

        while True:
            distance = round(self.sensor_desk.distance * 100)
            print('desk: ', distance)
            if distance < target_height:
                self.servo.angle = self.servo_up
            elif distance > target_height:
                self.servo.angle = self.servo_down
            else:
                self.servo.angle = self.servo_reset
                break
            time.sleep(0.3)  # Add a small delay to allow sensor to update and prevent tight loop

    def move_linear_save(self, target_height):
        while True:
            distance = round(self.sensor_laptop.distance * 100)
            print('stand: ', distance)
            if distance < target_height:
                self.motor.forward()
            elif distance > target_height:
                self.motor.backward()
            else:
                self.motor.stop()
                break
            time.sleep(0.3)  # Add a small delay to allow sensor to update and prevent tight loop

    def move_servo_manual(self, direction):
        if direction == 'up':
            self.servo.angle = self.servo_up
            time.sleep(0.3)
            self.servo.angle = self.servo_reset
            time.sleep(0.4)
        elif direction == 'down':
            self.servo.angle = self.servo_down
            time.sleep(0.3)
            self.servo.angle = self.servo_reset
            time.sleep(0.4)

        if direction == 'up':
            self.servo.angle = self.servo_up
        elif direction == 'down':
            self.servo.angle = self.servo_down

    def move_linear_manual(self, direction):
        if direction == 'up':
            self.motor.forward()
        elif direction == 'down':
            self.motor.backward()

    def stop_servo(self):
        self.servo.angle = self.servo_reset
        time.sleep(0.3)
        #self.servo.close()
        return round(self.sensor_desk.distance * 100)

    def stop_linear(self):
        self.motor.stop()
        time.sleep(0.3)
        #self.motor.close()
        return round(self.sensor_laptop.distance * 100)

    def return_height(self, target):
        if target == 'desk':
            return round(self.sensor_desk.distance * 100)
        elif target == 'laptop':
            return round(self.sensor_laptop.distance * 100)

    # 핀 할당 해제
    def finish(self):
        self.servo.angle = self.servo_reset
        time.sleep(0.3)
        self.motor.stop()
        time.sleep(0.3)

        # 모든 장치 닫기 및 리소스 해제
        if hasattr(self, 'servo') and self.servo is not None:
            self.servo.close()
        if hasattr(self, 'enA') and self.enA is not None:
            self.enA.close()
        if hasattr(self, 'motor') and self.motor is not None:
            self.motor.close()
        if hasattr(self, 'sensor_desk') and self.sensor_desk is not None:
            self.sensor_desk.close()
        if hasattr(self, 'sensor_laptop') and self.sensor_laptop is not None:
            self.sensor_laptop.close()


class ServoController(QObject):
    # pass

    def __init__(self):
        super().__init__()
        self.servo_motor = ServoMotor()

    @Slot()
    def start(self):
        self.servo_motor.initialization()

    @Slot(str)
    def move_desk(self, direction):
        self.servo_motor.move_servo_manual(direction)

    @Slot(str)
    def move_stand(self, direction):
        self.servo_motor.move_linear_manual(direction)

    @Slot(result=int)
    def stop_desk(self):
        return self.servo_motor.stop_servo()

    @Slot(result=int)
    def stop_stand(self):
        return self.servo_motor.stop_linear()

    @Slot(str, result=str)
    def update_height(self, target):
        return str(self.servo_motor.return_height(target))

    @Slot()
    def stop(self):
        self.servo_motor.finish()
        
    @Slot(int)
    def save_desk(self, height):
        self.servo_motor.move_servo_save(height)
     
    @Slot(int)
    def save_stand(self, height):
        self.servo_motor.move_linear_save(height)  
