from ckzn_gpio import Pin
#from Chirial import Chirial
from ckzn_web import WebIO
from wifi_client import WifiClient
from wifi_ap import WifiAP
from variable import *
import keyboard
import time, sys

#インスタンス生成
status: int = 0 #ステータス変数
pre_status: int = 1
new_serial_data: list = []
ap_mode: bool = False
manual_mode: bool = True
auto_mode: bool = True
current_mode: int = START_MODE
send_time:int = 20  #IR送信時間
ir_start_time:int = 0
#インスタンス生成
digital_io = Pin()
#serial_io = Chirial()
http_io = WebIO()
wifi_client = WifiClient()
wifi_ap = WifiAP()
#前処理
#wifi_ap.disconnect()
#wifi_client.connect()
try:

    #メインループ
    while(True):
        digital_io.check_condition()
        #---ステータス変更部---
        #APモード起動
        sw_mode = digital_io.check_mode()
        if (sw_mode==SETTING_MODE and current_mode!=SETTING_MODE):
            print("SETTING_MODE_INITIALIZING...")
            wifi_ap.connect()
            wifi_client.disconnect()
            current_mode=SETTING_MODE
            print("SETTING_MODE_STARTED.")

        #手動モード起動
        elif sw_mode==MANUAL_MODE and current_mode!=MANUAL_MODE:
            print("MANUAL_MODE_INITIALIZING...")
            if (current_mode==SETTING_MODE or current_mode==START_MODE):
                wifi_ap.disconnect()
                wifi_client.reconnect()
            status = 0
            current_mode=MANUAL_MODE
            print("MANUAL_MODE_STARTED.")

        #自動モード起動
        elif sw_mode==AUTO_MODE and current_mode!=AUTO_MODE:
            print("AUTO_MODE_INITIALIZING...")
            if (current_mode==SETTING_MODE or current_mode==START_MODE):
                wifi_ap.disconnect()
                wifi_client.reconnect()
            status = 0
            current_mode=AUTO_MODE
            print("AUTO_MODE_STARTED.")

        #自動モード動作
        if current_mode == AUTO_MODE:
            if digital_io.check_detector():
                status = INDOORS
            else:
                status = OUTDOORS

        #MANUAL MODE
        if (current_mode==MANUAL_MODE and digital_io.read_button()!=None):
            status = digital_io.read_button()
            print(status)

        #---LED出力/Webサーバに反映---
        if pre_status != status:
            pre_status=status
            print(pre_status)
            digital_io.set_led_stat(status)
            if current_mode!=SETTING_MODE:
                buf = wifi_client.read_proxy()
                try:
                    if http_io.post_status(status,proxy=buf)!=None:
                        print("OK!")
                        pre_status = 5
                except:
                    pass

        #IR通信を受信したら
        if digital_io.check_ir_recv() and ir_start_time==0:
            ir_start_time=time.time()
            digital_io.set_ir_stat(status)
        
        #IR停止タイマー動作
        if ir_start_time==0 :   
            diff= time.time()-ir_start_time
            if diff > send_time:
                digital_io.reset_ir_stat()
                ir_start_time = 0
        #KeyboardOut
        if keyboard.is_pressed("escape"):
            break

except KeyboardInterrupt:
       sys.exit(0)
