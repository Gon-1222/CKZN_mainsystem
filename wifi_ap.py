import subprocess, shlex
class WifiAP():

    #WiFi起動
    def connect(self):
        args = shlex.split("sudo ip link set ap0 up")
        ret = subprocess.call(args)
        if ret:
            return False
        print("server.py")
        #args = shlex.split("sudo python server.py")
        #self.proc = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        return True

    #WiFi切断
    def disconnect(self):
        args = shlex.split("sudo ip link set ap0 down")
        ret = subprocess.call(args)
        if ret:
            return False
        #try:
         #   self.proc.kill()
        #except:
         #   pass

        return True
if __name__=="__main__":
    tester=WifiAP()
    print(tester.connect())
    input("エンター押してね！")
    tester.disconnect()
