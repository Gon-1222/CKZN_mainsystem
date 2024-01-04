from ckzn_gpio import Pin
from Chirial import Chirial
from ckzn_web import WebIO
from wifi_client import WifiClient
from wifi_ap import WifiAP
import time

#インスタンス生成
status: int = 0 #ステータス変数
pre_status: int = 1
new_serial_data: list = []
ap_mode: bool = False
manual_mode: bool = True
auto_mode: bool = True
#インスタンス生成
digital_io = Pin()
serial_io = Chirial()
http_io = WebIO()
wifi_client = WifiClient()
wifi_ap = WifiAP()

#前処理
wifi_ap.disconnect()
wifi_client.connect()

#メインループ
while(True):
    digital_io.check_condition()
    #---ステータス変更部---
    #APモード起動
    auto_mode_sw = not(digital_io.digital_read("modevhanger2") or digital_io.digital_read("mode_changer1"))
    if digital_io.digital_read("mode_changer1") and ap_mode==False:
        wifi_ap.connect()
        wifi_client.disconnect()
        ap_mode,manual_mode,auto_mode = True,False,False
    #手動モード起動
    elif digital_io.digital_read("modevhanger2") and manual_mode==False:
        wifi_ap.disconnect()
        wifi_client.reconnect()
        status=digital_io.read_button()
        ap_mode, manual_mode,auto_mode = False, True, False
    #自動モード起動
    elif auto_mode_sw and auto_mode == False:
        wifi_ap.disconnect()
        wifi_client.reconnect()       
        if digital_io.digital_read("detector"):
            status=0
        else:
            status=1
    
    #シリアル通信（AP時のみ）
    if ap_mode:
        serial_data = serial_io.read_data()
        if serial_data:
            if serial_data[0]=="2" and serial_data[1] == "1":
                new_serial_data = serial_data[2:]
            if serial_data[1] == "2" and serial_data[1] == "2":
                new_serial_data.append(serial_data[2:])
                if len(new_serial_data)==5:
                    wifi_client.set_data(new_serial_data)
            if serial_data[0] in ["1","2"]:
                current_serial_data = wifi_client.read_data()
                if serial_data[1]=="1":
                    serial_io.wifi_write_data(current_serial_data[0],
                                          current_serial_data[1],
                                          current_serial_data[2])
                if serial_data[1]=="2":
                    serial_io.http_write_data(current_serial_data[3],
                                          current_serial_data[4])



    #---LED出力/Webサーバに反映---
    if pre_status!=status:
        digital_io.set_led_stat(status)
        if not(ap_mode):
            buf = wifi_client.read_proxy()
            http_io.post_status(status,proxy=buf)

    #IR通信を受信したら
    if digital_io.digital_read("recv") and ir_start_time==0:
        ir_start_time=time.time()
        digital_io.set_ir_stat(status)
    
    #IRタイマー動作
    if ir_start_time==0 :   
        diff= time.time()-ir_start_time
        if diff > 20:
            digital_io.reset_ir_stat()
            ir_start_time = 0
    