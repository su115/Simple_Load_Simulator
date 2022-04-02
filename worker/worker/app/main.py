#! /bin/python3
class WRequest:
    cname = "WRequests:"
    def __init__(self,headers=None):
        self.headers = self.check_headers(headers)
        
    def check_headers(self,headers):
        if headers == None:
            # headers is not set
            return headers
        # check type == dict
        if type(headers) != type(dict()):
            raise ValueError(cname+"headers is not dict!!!")
        # check dict( key,values ) == str
        for key,value in headers:
                if type(key) != type(str()) or type(value) != type(str):
                    raise ValueError(cname+"headers is dict but one of values is not str!!!")
        return headers



# Test request
#url = 'http://localhost:80/'
#header = {"my":"123"}
#
#import requests
#req = requests.get(url,headers=header)
#print(dir(req))
#print("elapsed:\t",req.elapsed)
#print("history:\t",req.history)
#print("headers:\t",str(req.headers))
#print("status_code:\t",str(req.status_code))
