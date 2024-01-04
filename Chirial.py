import serial

class Chirial:

    def __init__(self,com,baud=9600) -> None:
        global serial1
        serial1 = serial.Serial(com, baud, timeout=5, bytesize=8, parity=serial.PARITY_ODD, xonxoff=True,stopbits=1)
        return
    def __del__(self):
        serial1.close()
        return

    def read_data(self) -> list:
        data = serial1.read(512).decode()
        if data == "":
            return None
        try:
            data = data[4:data.index(';')].replace(' ', '').split(',')
        except:
            return None
        if len(data) < 2:
            return [0,0]
        
        return data

    def wifi_write_data(self,network,user,password) -> int:
        data = "res 1," + network + "," + user+ "," + password + ";"
        print(data)
        serial1.write(data.encode("UTF-8"))
        return 0

    def http_write_data(self,domain,port) -> int:
        data = "res 1," + domain + ","+ port + ";"
        serial1.write(data.encode("UTF-8"))
        return 0


if __name__=="__main__":

    ser = Chirial("COM9")

    while(True):
        data = ser.read_data()
        print(data)
        if not(data):
            continue

        if data[0]=="2":
            print(data)#データをセットする

        if data[0] in ["1","2"]:
            if data[1]=="1":
                ser.wifi_write_data("example","st****aa","password")
            if data[1]=="2":
                ser.http_write_data("domain","port")