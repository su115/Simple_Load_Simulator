from worker.app.WReq import WRequest
from worker.app.CReq import CRequest
from worker.variables import *
import uuid


class WSession:
    def __init__(self, block):
        self.name = block["name"]
        self.port = block["port"]
        self.protocol = block["protocol"]
        self.ip = block["ip"]
        self.proxies = block["proxies"] if "proxies" in block else None
        self.verify = block["verify"] if "verify" in block else True  # https
        self.timeout = block["timeout"] if "timeout" in block else (1, 3)
        self.allow_redirects = (
            block["allow_redirects"] if "allow_redirects" in block else False
        )
        self.list_wreq = []  # block['list_req']
        self.dict_creq = {}
        self.list_resaults = []  # here we save resaults
        for req in block["list_req"]:
            salt = str(uuid.uuid4())[:6]
            url = f"""{self.protocol}://{self.ip}{self.port}{req["location"]}"""
            cname = self.name + "-creq-" + salt
            wname = self.name + "-wreq-" + salt
            #print("init:")
            #print("\tcname:", cname)
            #print("\twname:", wname)
            #print("\turl:  ", url)
            creq = CRequest(
                name=cname,
                salt=salt,
                posible_status_code=req["posible_status_code"]
                if "posible_status_code" in req
                else None,  # list
                expected_status_code=req["expected_status_code"],
                expected_text=req["expected_text"] if "expected_text" in req else None,
                expected_headers=req["expected_headers"]
                if "expected_headers" in req
                else None,
            )
            wreq = WRequest(
                name=wname,
                url=url,
                # print a if b else 0
                method=req["method"] if "method" in req else "GET",
                headers=req["headers"] if "headers" in req else None,
                data=req["data"] if "data" in req else None,
                params=req["params"] if "params" in req else None,
                delay=req["delay"] if "delay" in req else 0.0,
            )
            self.list_wreq.append(wreq)
            self.dict_creq[cname] = creq

    def send(self):
        for wreq in self.list_wreq:
            answer = wreq.send(
                proxies=self.proxies,
                verify=self.verify,
                timeout=self.timeout,
                allow_redirects=self.allow_redirects,
            )
            resault = self.check_resault(wreq, answer)
            self.list_resaults.append(resault)

    def check_resault(self, wreq, answer):
        resault = {}
        resault["error"] = []

        # GET names
        cname = wreq.name.replace("wreq-", "creq-")
        #print("check_resaults:")
        #print("\tcname:", cname)
        #print("\twname:", wreq.name)
        resault["cname"] = cname
        resault["wname"] = wreq.name
        creq = self.dict_creq[cname]

        if creq.posible_status_code != None:
            if not answer.status_code in creq.posible_status_code:
                err = f""" answer.status_code: {answer.status_code} 
                     posible_status_code: {creq.posible_status_code}
                """  # not exist in posible stats_code
                resault["error"].append(err)
        if creq.expected_status_code != answer.status_code:
            err = f""" expected_status_code: {creq.expected_status_code} 
                     answer_status_code: {answer.status_code}
                """
            resault["error"].append(err)
        if creq.expected_text != None:
            if creq.expected_text != answer.text:
                err = f""" expected_text: {creq.expected_text}
                     answer.text: {answer.text}
                 """
                resault["error"].append(err)
        if creq.expected_headers != None:

            #Try transforming the CaseInsensitiveDict to a plain old dict, like so:
            #json.dump(dict(data), file)
            # if not expected is part of answer
            if not creq.expected_headers.items() <= dict(answer.headers).items():
                err = f""" expected_headers: {creq.expected_headers}
                     answer.headers: {answer.headers}
                 """
                resault["error"].append(err)
        return resault
