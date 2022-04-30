#! /bin/python3
import requests
import validators
import uuid
class WRequest:
    cname = "WRequests:"
    url="http://localhost:80"
    method="GET"
    instance=None
    data=None 
    headers=None
    proxies=None
    params=None
    name='None'
    #proxies = None   # dict    #proxies = { 'http' : 'https://user:password@proxiesip:port' }

    def __init__(self,
            url="http://localhost:80",
            method="GET",
            instance=None,
            data=None, 
            headers=None,
            proxies=None,
            params=None,
            name='None',
            ):

        # name 
        if name=='None':
                self.name='wreq-'+str(uuid.uuid4)
        else:
                self.name=name

        self.prepped = None
        self.headers = self._check_dict(headers,"headers")
        self.data = self._check_dict(data,"data") 
        self.params = self._check_dict(params,"params")
        
        #method
        if self._is_type( method,str) and  method in ["GET","POST","DELETE","PATCH","PUT"]:
            self.method = method # Checked
        else:
            self._init_value_error(method,"method")

        #instance
        if  instance == None or self._is_type(instance, requests.Session): # for testing purposes
            if instance == None:
                print("New session instance")
                self.instance = requests.Session() # Checked
            else:
                print("Custom session instance")
                self.instance = instance
        else:
            print(type(instance))
            self._init_value_error(instance,"instance")
       
        #proxies
        self.proxies = self._check_dict(proxies,"proxies")

        #url
        if self._is_type(url,str) and  validators.url(url):
            self.url =  url
        else:
            self._init_value_error(url,"url")

        # instance not None
        #if self.instance == None:
        #    raise ValueError("problems with instance.")

    def __del__(self):
        if not self.instance == None:
            print(self.instance,'\t',str(type(self.instance)))
            self.instance.close() # Double delete :(
        self.instance = None
        self.data=None
        self.method = None
        self.headers = None
        self.proxies = None
        self.url = None
        self.prepped = None

    def _init_value_error(self,value,what):
            raise ValueError(what +" is incorect:" + str(type(value)) + str(value) )

    def _check_list(self,data,list_name):
        if  data == None: 
                return data 
        elif self._is_type(data,list):
            for string in data:
                if not ( self._is_type(string,str)  ):
                    self._init_value_error(string,"string")
            return data
        else:
                    self._init_value_error(data,list_name)
        

    def _make_prepped(self): # Not checked
        req = requests.Request(
                method=self.method,
                url=self.url, 
                headers=self.headers,
                data=self.data,
                params=self.params,
                #proxies=self.proxies,
                )
        self.prepped = req.prepare()
        return self.prepped

    def send(self): # Not checked
        if self.prepped == None:
            self._make_prepped()
        
        answer = self.instance.send(
                self.prepped,
                proxies=self.proxies,
                verify=False, # hard                
                timeout=(1, 5), # hard (connect, read)
                )
        return answer
   
    def _check_dict(self, dct, dict_name):
        if dct == None:
            return dct
        if not self._is_type(dct,dict):
            value = str(type(dct))
            raise ValueError(self.cname + f'''type of varriable \"{dict_name}\" is {value} ''')
        for key in dct:
            if not (  self._is_type(key,str) and  self._is_type(dct[key],str) ):
                    t1 = str(type(key))
                    t2 = str(type(dct[key]))
                    raise ValueError(self.cname+f"""{dict_name} is dict but one of values is not str!!!
                            key:\t{key}\t{t1}
                            value:\t{dct[key]}\t{t2}
                            """)
        return dct

    def _is_type(self,value, func):
        if type(value) is func:
            return True
        return False

    def got_yaml(self,data):
            if self.instance == None:
                self.instance = requests.Session() # Checked
            if 'name' in data:
                self.name=data['name']
            if "headers" in data:
                self.headers=data["headers"]
            if 'method' in data:
                self.method=data["method"]
            if 'url' in data:
                self.url=data['url']
            if 'data' in data:
                self.data=data['data']
            if 'params' in data:
                self.params=data['params']
    def get_status(self):
        print('='*23)
        print( f"""
        name:\t\t{self.name}
        data:\t\t{self.data}
        params:\t\t{self.params}
        method:\t\t{self.method}
        headers:\t{self.headers}
        proxies:\t{self.proxies}
        url:\t\t{self.url}
        """)
        print("="*23)
    def set_proxies(self,proxies):
            if self.instance == None:
                self.instance = requests.Session() # Checked
            self.proxies=self._check_dict(proxies,"proxies")

        
