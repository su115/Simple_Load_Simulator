#! /bin/python3
import requests
import validators
import uuid
import time

class WRequest:
    cname = "WRequests:"
    url = "http://localhost:80"
    method = "GET"
    instance = None
    data = None
    headers = None
    params = None
    name =  "None" 

    def __init__(
        self,
        url: str="http://localhost:80",
        method: str="GET",
        instance: requests.Session=None,
        data:dict[str]=None,
        headers:dict[str]=None,
        params:dict[str]=None,
        name: str="None",
        delay:float=0.0,
    ):
        self.delay  =  delay
        # name
        if name == "None":
            self.name = "wreq-" + str(uuid.uuid4())[:6]
        else:
            self.name = name
        # prepped
        self.prepped = None
        self.headers = headers
        self.data = data
        self.params = params

        # method
        if  method in [
            "GET",
            "POST",
            "DELETE",
            "PATCH",
            "PUT",
        ]:
            self.method = method  # Checked
        else:
            self._init_value_error(method, "method")

        # instance
        if instance == None or self._is_type(
            instance, requests.Session
        ):  # for testing purposes
            if instance == None:
                self.instance = requests.Session()  # Checked
            else:
                print("Custom session instance")
                self.instance = instance
        else:
            print(type(instance))
            self._init_value_error(instance, "instance")
        # url
        if self._is_type(url, str) and validators.url(url):
            self.url = url
        else:
            self._init_value_error(url, "url")

        
    def __del__(self):
        if not self.instance == None:
            print(self.instance, "\t", str(type(self.instance)))
            self.instance.close()  # Double delete :(
        self.instance = None
        self.data = None
        self.method = None
        self.headers = None
        self.url = None
        self.prepped = None

    def _init_value_error(self, value, what):
        raise ValueError(what + " is incorect:" + str(type(value)) + str(value))

    def _make_prepped(self):  # Not checked
        req = requests.Request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            data=self.data,
            params=self.params,
            # proxies=self.proxies,
        )
        self.prepped = req.prepare()
        return self.prepped

    def send(self,verify=False,timeout=(1,5),proxies=None,allow_redirects=False):  # Not checked
        if self.prepped == None:
            self._make_prepped()

        answer = self.instance.send(
            self.prepped,
            proxies=proxies,
            verify=verify,  # hard
            timeout=timeout,  # hard (connect, read)
            allow_redirects=allow_redirects,
        )
        if self.delay != 0.0:
            time.sleep(self.delay)
        return answer

    def _is_type(self, value, func):
        if type(value) is func:
            return True
        return False

    # Delete ???
    def got_yaml(self, data):
        if self.instance == None:
            self.instance = requests.Session()  # Checked
        if "name" in data:
            self.name = data["name"]
        if "headers" in data:
            self.headers = data["headers"]
        if "method" in data:
            self.method = data["method"]
        if "url" in data:
            self.url = data["url"]
        if "data" in data:
            self.data = data["data"]
        if "params" in data:
            self.params = data["params"]

    def get_status(self):
        print("=" * 23)
        print(
            f"""
        name:\t\t{self.name}
        data:\t\t{self.data}
        params:\t\t{self.params}
        method:\t\t{self.method}
        headers:\t{self.headers}
        url:\t\t{self.url}
        """
        )
        print("=" * 23)

