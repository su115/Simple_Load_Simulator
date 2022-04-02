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
            raise ValueError(self.cname+"headers is not dict!!!")
        # check dict( key,values ) == str
        for key in headers:
                if not type(key) == type(str()) and type(headers[key]) == type(str):

                    t1 = str(type(key))
                    t2 = str(type(headers[key]))
                    raise ValueError(self.cname+f"""headers is dict but one of values is not str!!!
                            key:\t{key}\t{t1}
                            value:\t{headers[key]}\t{t2}
                            """)
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
