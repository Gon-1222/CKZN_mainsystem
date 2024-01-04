import requests
class WebIO():
    _api_domain = "https://example.com"
    _request_pass = _api_domain + "/machine"
    #GET動作
    def get_status(self,proxy=None):
        if proxy:
            proxies = {
            "http": proxy,
            "https": proxy
            }
            response = requests.get(self._request_pass,proxies=proxies)
        else:
            response = requests.get(self._request_pass)
        if response.status_code!=200:
            return None
        
        return response.json()["status"]
    
    #POST動作
    def post_status(self,status,proxy=None):
        if proxy:
            proxies = {
            "http": proxy,
            "https": proxy
            }
            response = requests.post('http://www.example.com', data={'status': status},proxies=proxies)
        else:
            response = requests.post('http://www.example.com', data={'status': status})

        if response.status_code!=200:
            return None
        if response.json()["message"] != "success":
            return None
        
        return True

if __name__=="__main__":
    tester=WebIO()
    print("get:",tester.get_status())
