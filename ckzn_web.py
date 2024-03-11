import requests
from variable import *

class WebIO():
    _api_domain = "https://chikuzenni-api.vercel.app"
    _request_pass = _api_domain + "/machine"
    #GET動作
    def get_status(self,proxy=None):
        headers = {
            'machine_ID': MACHINE_ID
         }
        if proxy:
            proxies = {
            "http": proxy,
            "https": proxy
            }
            response = requests.get(self._request_pass,headers=headers,proxies=proxies)
        else:
            response = requests.get(self._request_pass,headers=headers)
        if response.status_code!=200:
            return None
        
        return response.json()["status"]
    
    #POST動作
    def post_status(self,status,proxy=None):
        print("POST")
        headers = {
        'machine_ID': MACHINE_ID,
        'COntent-Type':'application/json'
        } 
        if proxy:
            proxies = {
            "http": proxy,
            "https": proxy
            }
            try:
                response = requests.post(self._request_pass ,headers=headers, json={'status': status},proxies=proxies,timeout=(2.0,2.0))
            except:
                print("Timeout")
                return None
        else:
            try:
                response = requests.post(self._request_pass ,headers=headers, json={'status': status},timeout=(2.0,2.0))
            except:
                print("Timeout")
                return None

        if response.status_code!=200:
            print("Status Error")
            return None
        print("success POST")
        return True

if __name__=="__main__":
    tester=WebIO()
    print("get:",tester.get_status())
