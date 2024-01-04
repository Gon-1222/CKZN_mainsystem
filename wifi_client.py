import subprocess, shlex
class WifiClient():
    _data=[]

    #設定取得
    def __init__(self):
        self.read_data()
        return None
    
    #データ読み込み
    def read_data(self):
        with open("wifi_client.dat",mode="r") as f:
            self._data=[s.rstrip() for s in f.readlines()]
        return True
    
    #データ保存
    def save_data(self):
        with open("wifi_client.dat",mode="w") as f:
            f.writelines(map(lambda x: x+ "\n",self._data))
        # with open("/etc/wpa_supplicant/wpa_supplicant.conf",mode="w") as f:
        #     f.write(self._generate_wpa_conf())
        return True

    #WiFi設定
    def set_data(self,data):
        self._data=data
        self.save_data()
        return True

    #WiFi設定取得
    def check_data(self):
        return self._data
        
    def read_proxy(self):
        if self._data[3] and self._data[4]:
            return self._data[3]+":"+self._data[4]
        return None
    #再接続
    def reconnect(self):
        self.read_data()
        return self.connect()


    #WiFi接続
    def connect(self):
        return self.connect_to_wifi()



    #WiFi切断
    def disconnect(self):
        args = shlex.split("sudo ifconfig wlan0 down")
        ret = subprocess.call(args)
        if ret:
            return False
        return True
    
    def connect_to_wifi(self):
        ssid=self.data[0]
        identity=self.data[1]
        password=self.data[2]

        # 新しいネットワーク情報を作成
        network_info = f'network={{\n\tssid="{ssid}"\n'

        if not(identity) and password:
            network_info += f'\tpsk="{password}"\n'

        if identity and password:
            network_info += f'\tkey_mgmt=WPA-EAP\n\teap=PEAP\n\tidentity="{identity}"\n\tpassword="{password}"\n\tphase1="peaplabel=0"\n\tphase2="auth=MSCHAPV2"\n'

        network_info += '}'

        # wpa_supplicant.confを書き換え
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as file:
            file.write(network_info)

        # WiFi設定を再読み込みして変更を反映
        subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'])
        return True
if __name__=="__main__":
    import requests
    tester=WifiClient()
    print("セットデータ")
    
    print(tester.check_data())
    print("接続")
    tester.connect()
    print(tester.read_proxy())
    proxies = {
            "http":"http://"+tester.read_proxy(),
            "https":"http://"+tester.read_proxy()
    }
    response = requests.get("https://example.com", proxies=proxies, timeout=5)
    print(200==response.status_code)
    print("切断")
    tester.disconnect()

    # 使用例（一般的な方式）
    #connect_to_wifi('YourWiFiNetworkName', 'YourWiFiPassword')

    # 使用例（エンタープライズ方式）
    #connect_to_wifi('YourEnterpriseNetworkName', None, 'YourUsername', 'YourEnterprisePassword')