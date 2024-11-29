import subprocess
import sys
from PySide6.QtCore import QObject, Slot, Signal, QThread
from time import sleep, time
import threading
import os
import random
from deskStandData import DeskStandData

class ScriptWorker(QThread):
    finished = Signal()  # 작업 완료 시그널

    def __init__(self, deskStandData: DeskStandData, parent=None):
        super().__init__(parent)
        self.deskStandData = deskStandData
        self.local_script_path = self._get_local_script_path()

    def _get_local_script_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        return os.path.join(parent_dir, "total_test.py")

    def run(self):
        try:
            self._runScript()
        except Exception as e:
            print(f"An error occurred during script execution: {e}")

    def _runScript(self):
        # 무작위로 포트 번호 생성 (0부터 65535 범위 내에서)
        port_number = random.randint(0, 65535)

        # 원격 서버에서 파이썬 스크립트 실행
        remote_command = ["ssh", "orin@192.168.137.196", "xvfb-run", "-a", "python3", "/home/orin/test/new_total.py", str(port_number)]

        # 로컬에서 파이썬 스크립트 실행
        local_command = ["python3", self.local_script_path, str(port_number)]

        try:
            # 두 개의 명령어를 동시에 실행
            process1 = subprocess.Popen(remote_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print('popen1 started')
            sleep(5)
            process2 = subprocess.Popen(local_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print('popen2 started')

            output_thread = threading.Thread(target=self._read_process_output, args=(process2,))
            output_thread.start()

            self._monitor_processes(process1, process2, output_thread)

            self.finished.emit()  # 작업 완료 시그널 발생

        except Exception as e:
            print(f"An error occurred during script execution: {e}")

    def _read_process_output(self, process):
        try:
            welcome_check = False
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print('process2 output:', output.strip())
                    sys.stdout.flush()
                    
                    if welcome_check:
                        # desk_height와 stand_height 값을 stdout2에서 추출하여 deskStandData에 저장
                        desk_height, stand_height = list(map(int, output.split()))
                        self.deskStandData.deskHeight = desk_height
                        self.deskStandData.standHeight = stand_height
                        welcome_check = False
                        print(self.deskStandData.deskHeight, self.deskStandData.standHeight)
                    
                    if 'Welcome!' == output.strip():
                        welcome_check = True
                    
                    
        except Exception as e:
            print(f"Error reading process output: {e}")

    def _monitor_processes(self, process1, process2, output_thread):
        start_time = time()
        timeout = 20

        try:
            while True:
                if process2.poll() is not None:
                    stdout2, stderr2 = process2.communicate()
                    print('process2 finished with return code:', process2.returncode)
                    print('process2 stdout:', stdout2)
                    print('process2 stderr:', stderr2)

                    break

                if time() - start_time > timeout:
                    print("Process2 did not finish in time and will be terminated.")
                    process2.terminate()
                    output_thread.join()
                    stdout2, stderr2 = process2.communicate()
                    print('process2 terminated due to timeout.')
                    print('process2 stdout:', stdout2)
                    print('process2 stderr:', stderr2)
                    break

                sleep(1)

            # Check process1
            stdout1, stderr1 = process1.communicate()
            print('process1 stdout:', stdout1)
            print('process1 stderr:', stderr1)

        except Exception as e:
            print(f"Error during process monitoring: {e}")

class PyInterface(QObject):
    scriptFinished = Signal()

    def __init__(self, deskStandData: DeskStandData):
        super().__init__()
        self.worker_thread = ScriptWorker(deskStandData)
        self.worker_thread.finished.connect(self.onScriptFinished)

    @Slot()
    def runScript(self):
        print("Starting script...")
        self.worker_thread.start()

    @Slot()
    def onScriptFinished(self):
        print("Script execution finished.")
        self.scriptFinished.emit()
