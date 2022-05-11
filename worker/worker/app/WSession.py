from worker.app.WReq import WRequest
from worker.app.CReq import CRequest
from worker.variables import *
import uuid, requests


class WSession:
    def __init__(self, block):
        # INPUT
        # block is dict
        # required fields:
        #   'name'
        #   'ip'
        #   'list_req'
        #       'location'
        #       'expected_status_code'
        #       
        # OUTPUT
        # list_resaults
        self._check_reqired_params(block)
        self.name = block["name"]
        self.port = block["port"] if 'port' in block else ''
        self.protocol = block["protocol"] if 'protocol' in block else 'http'# 'http' or 'https'
        self.ip = block["ip"]                                               # ip or dnsname required
        self.proxies = block["proxies"] if "proxies" in block else None
        self.verify = block["verify"] if "verify" in block else True  # https
        self.timeout = block["timeout"] if "timeout" in block else (7, 15) #(1, 3)
        self.allow_redirects = (
            block["allow_redirects"] if "allow_redirects" in block else False
        )
        self.list_wreq = []  # block['list_req']
        self.dict_creq = {}
        self.list_resaults = []  # here we save resaults
       # self.list_resaults.append(self.name)
        for req in block["list_req"]:
            if "name" in req: ### if name exists in yaml
                cname = req['name']
                wname = req['name']
                salt = ''
            else: ### if not lets generate :)
                salt = str(uuid.uuid4())[:6]            
                cname = self.name + "-request-" + salt
                wname = cname

            url = f"""{self.protocol}://{self.ip}{self.port}{req["location"]}"""
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
                expected_status_code=req["expected_status_code"],                       # reqired
                expected_text=req["expected_text"] if "expected_text" in req else None,
                expected_headers=req["expected_headers"]
                if "expected_headers" in req
                else None,
            )
            wreq = WRequest(
                name=wname,                 # generated
                url=url,                    # reqired -> protocol, ip, port, req['location']
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
            try:
                answer = wreq.send(
                    proxies=self.proxies,
                    verify=self.verify,
                    timeout=self.timeout,
                    allow_redirects=self.allow_redirects,
                )
                resault = self.check_resault(wreq, answer)
                self.list_resaults.append(resault)
            except requests.exceptions.ConnectionError:
                message = "ConnectionError:   " + wreq.url
                resa = self._create_error(wreq)
                resa['error'].append(message)
                self._print_error_position(wreq, message)
                self.list_resaults.append(resa)
                
                
    def _create_error(self, wreq):
        resault = {}
        resault['error'] = []
        resault['name'] = wreq.name
        return resault

    def check_resault(self, wreq, answer):
        resault = self._create_error(wreq)
        #resault["error"] = []

        # GET names
        cname = wreq.name # .replace("-wreq-", "-creq-")
        #print("check_resaults:")
        #print("\tcname:", cname)
        #print("\twname:", wreq.name)
        #resault["cname"] = cname
        #resault["wname"] = wreq.name
        creq = self.dict_creq[cname]

        if creq.posible_status_code != None:
            if not answer.status_code in creq.posible_status_code:
                
                err = f"""answer.status_code: {answer.status_code} posible_status_code: {creq.posible_status_code}"""  # not exist in posible stats_code
                self._print_error_position(wreq,err)
                resault["error"].append(err)
        if creq.expected_status_code != answer.status_code:
            err = f"""expected_status_code: {creq.expected_status_code} answer_status_code: {answer.status_code}"""
            self._print_error_position(wreq,err)
            resault["error"].append(err)
        if creq.expected_text != None:
            if creq.expected_text != answer.text:
                err = f"""expected_text: {creq.expected_text}  answer.text: {answer.text}"""
                self._print_error_position(wreq,err)
                resault["error"].append(err)
        if creq.expected_headers != None:

            #Try transforming the CaseInsensitiveDict to a plain old dict, like so:
            #json.dump(dict(data), file)
            # if not expected is part of answer
            if not creq.expected_headers.items() <= dict(answer.headers).items():
                err = f"""expected_headers: {creq.expected_headers}  answer.headers: {answer.headers}"""
                self._print_error_position(wreq,err)
                resault["error"].append(err)
        return resault

    def _print_error_position(  self,
                                wreq,   # str or WRequest 
                                err     # str
                                ):
        
        print('-'*18)
        msg = ''
        if  type(wreq) == type(str()):### when validation error
            msg += wreq
        else:### when normal error
            msg += f"Session name: {self.name};  " 
            msg += f"Request name: {wreq.name};  "
            msg += f"URL: {wreq.url};  "
        err = 'Error: '+err
        print(msg)
        print(err)
        print('-'*18)

    def _check_reqired_params(self,block):
        # INPUT
        # block is dict
        # required fields:
        #   'name'
        #   'ip'
        #   'list_req'
        #       'location'
        #       'expected_status_code'
        #       'name'                  #uniq !!!! or generated!!!
        req_main = ['name', 'ip', 'list_req']
        req_list_req = ['expected_status_code','location']
        for param in req_main:
            if not param in block:
                err=  f"Error: reqired '{param}' is not exists in block: {block}"
                self._print_error_position('missing reqired arg!!!',err)
                code = 422
                #print(err)
                raise Exception(err,code)
        for param in req_list_req:
            for req in block["list_req"]:
                if not param in req:
                    err= f"Error: reqired \"{param}\" is not exist in block['list_req']:{req}"
                    self._print_error_position('missing reqired arg!!!',err)
                    #print(err)
                    code = 422
                    raise Exception(err,code)
        list_name = []
        for req in block["list_req"]:
            if "name" in req:
                if not req['name'] in list_name:
                    list_name.append(req['name'])
                else:
                    err = f"Error: found dublicate of uniq field \"name\":"
                    names = ' '
                    for re in block['list_req']:
                        names += str(re['name']) if 'name' in re else "None"
                        names += ' '
                    err += names
                    self._print_error_position('Error dublicate!!!', err)
                    code = 422
                    raise Exception(err,code)
        

