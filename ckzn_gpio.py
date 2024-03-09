import time
from variable import *
import RPi.GPIO as GPIO
class Pin():
    #出力ピン番号
    _assign_out = {"send_d0":3,"send_d1":4,"send_d2":17,
                  "send_d3":27,"send_te":22,"send_ch1":10,
                  "send_ch2":9,"stat_out1":12,"stat_out2":6,
                  "stat_out3":13,"stat_out4":19,"stat_out5":26,
                  "err_out":16}
    #入力ピン番号
    _assign_in = {"recv":2,"mode_changer1":11,"mode_changer2":5,
                 "stat_in1":7,"stat_in2":8,"stat_in3":24,
                 "stat_in4":18,"stat_in5":23,"detector":20}

    #入力状態
    _input_condition = {}
    #出力状態
    _output_condition = {}

    #初期設定
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        #inputの設定
        buf = [val for val in self._assign_out.values()]
        GPIO.setup(buf,GPIO.OUT)
        #outputの設定
        buf = [val for val in self._assign_in.values()]
        GPIO.setup(buf,GPIO.IN)
        return

    #ピンを開放
    def __del__(self):
        GPIO.cleanup()
        return
    
    #入力の状態取得
    def check_condition(self):
        for key,val in self._assign_in.items():
            self._input_condition[key] = GPIO.input(val)
        return

    #入力状態のチェック
    def digital_read(self,pin_name):
        return self._input_condition.get(pin_name)
    
    #出力する
    def digital_write(self,pin_name,con):
        self._output_condition[pin_name]=con
        self._output_pin(pin_name)
        return

    #Writeの関数
    def _output_pin(self,pin_name):
        GPIO.output(self._assign_out[pin_name],self._output_condition[pin_name])
        return
    
    #人感センサ
    def check_detector(self):
        if self.digital_read("detector"):
            return True
        else:
            return False
    #モード確認
    def check_mode(self):
        if self.digital_read("mode_changer1"):
            return AUTO_MODE
        elif self.digital_read("mode_changer2"):
            return MANUAL_MODE
        else:
            return SETTING_MODE

    #LEDのステータス表示
    def set_led_stat(self,status):
        print(status)
        pattern = [[1 if row==col else 0 for col in range(5)] for row in range(5)]
        self.digital_write("stat_out1",pattern[status][0])
        self.digital_write("stat_out2",pattern[status][1])
        self.digital_write("stat_out3",pattern[status][2])
        self.digital_write("stat_out4",pattern[status][3])
        self.digital_write("stat_out5",pattern[status][4])
        return True

    #ir通信を受信する
    def check_ir_recv(self):
        if self.digital_read("recv"):
            return False
        else:
            return True

    #ir通信をスタートする
    def set_ir_stat(self,status):
        _ir_pin=[[1,0,1,0,0],
                [1,0,0,1,0],
                [1,0,0,0,1],
                [0,1,1,0,0],
                [0,1,0,1,0]]
        self.digital_write("send_ch1",_ir_pin[status][0])
        self.digital_write("send_ch2",_ir_pin[status][1])
        self.digital_write("send_d0",_ir_pin[status][2])
        self.digital_write("send_d1",_ir_pin[status][3])
        self.digital_write("send_d2",_ir_pin[status][4])
        self.digital_write("send_te",False)
        return True
    #ir通信を終了する
    def reset_ir_stat(self):
        self.digital_write("send_te",True)
        self.digital_write("send_ch1",False)
        self.digital_write("send_ch2",False)
        self.digital_write("send_d0",False)
        self.digital_write("send_d1",False)
        self.digital_write("send_d2",False)

    #ボタンの状態を取得する
    def read_button(self):
        if (self.digital_read("stat_in1")):
            return 0
        elif (self.digital_read("stat_in2")):
            return 1
        elif (self.digital_read("stat_in3")):
            return 2
        elif (self.digital_read("stat_in4")):
            return 3
        elif (self.digital_read("stat_in5")):
            return 4
        return None

if __name__=="__main__":
    tester=Pin()
    i=0
    while(True):
        i+=1
        tester.check_condition()
        buf = tester.read_button()
        print(f"\rボタンの状態：{buf}",end="")
        print(f"点灯中：",tester.set_led_stat(i%5),end="")
        time.sleep(0.5)
