from worker.app.WReq import WRequest
from worker.app.CReq import CRequest
from worker.variables import *
import uuid, requests


class WSession:
    def __init__(self, block):
        # INPUT 
        # block is dict
        # required fields:
        #   'name'-> not
        #   'ip'
        #   'list_req'
        #       'location'
        #       'expected_status_code'
        #       
        # OUTPUT
        # list_resaults



        self._check_reqired_params(block) # mandatory params
        #   'name' -> not mandatory
        #   'ip'
        #   'list_req'
        #       'location'
        #       'expected_status_code'
        #       'name' 
        
        # another
        #       'expected_text'
        #       'possible_status_code'
        #       'expected_headers'
        self.is_valid(block) #check additional params
        #   'port'
        #   'protocol'
        #   'timeout'
        #   'verify'
        #   'ip'

        self._check_bad_params(block)
        self.name = block["name"] if 'name' in block else "Session-"+ str( uuid.uuid4() )[:8]
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
        self.list_resaults.append(self.name)
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
    
    def is_valid(self,block):
        err = "Error: WSession: is_valid: "
        # port
        # protocol
        # timeout
        # verify
        # ip <-- str
        
        protocols = ['https','http']
        #check port        
        if 'port' in block:
            if not isinstance(block['port'],str):
                    raise Exception(err + f"parameter 'port' is '{block['port']}' but you need for example ':443' or ':80' or empty '' ",422)
            if  block['port'] == "" :
                pass
            elif  block['port'][0] == ':':
                if  block['port'][1:].isdigit():
                    pass
                else:
                    raise Exception(err + f"parameter 'port' is '{block['port']}' but you need for example ':443' or ':80' or delete this param.",422)
            else:
                raise Exception(err + f"parameter 'port' is '{block['port']}' but you need for example ':443' or ':80' or delete this param.",422)
        # check protocol
        if 'protocol' in block:
            if not isinstance(block['protocol'],str):
                raise Exception(err + f"parameter 'protocol' is '{block['protocol']}' but you need 'http' or 'https'.",422) 
            if not block['protocol'] in protocols:
                raise Exception(err + f"parameter 'protocol' is '{block['protocol']}' but you need 'http' or 'https'.",422)
        # timeout
        if 'timeout' in block:
            if   isinstance(block['timeout'],tuple) or  isinstance(block['timeout'], list):
                if len(block['timeout']) == 2:
                    if isinstance(block['timeout'][0],int) and isinstance(block['timeout'][1],int):
                        pass
                    else:
                        raise Exception(err + f"parameter 'timeout' is '{block['timeout']}' but you need for example '(1,2)' or '[1,2]'.",422)
                else:
                    raise Exception(err + f"parameter 'timeout' is '{block['timeout']}' but you need for example '(1,2)' or '[1,2]'.",422)
            else:
                raise Exception(err + f"parameter 'timeout' is '{block['timeout']}' but you need for example '(1,2)' or '[1,2]'.",422)
        # verify 
        if 'verify' in block:
            if not isinstance(block['verify'],bool):
                print("check 'verify'", block['verify'])
                raise Exception(err + f"parameter 'verify' is '{block['verify']}' but you need for example 'true' or 'false'",422)
        # ip
        if 'ip' in block:
            if not isinstance(block['ip'],str):
                raise Exception(err + f"parameter 'ip' is '{block['ip']}' but you need for example '192.168.0.2' or dnsname 'wiki.org'.",422)


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
        error = "Error: WSession: check_resault: "
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
        #   'ip'
        #   'list_req'
        #       'location'
        #       'expected_status_code'
        #       'name'                  #uniq !!!! or generated!!!
        req_main = [ 'ip', 'list_req']
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
                    err= f"Error: reqired '{param}' is not exist in block['list_req']:{req}"
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
                    err = f"Error: found dublicate of uniq field 'name:"
                    names = ' '
                    for re in block['list_req']:
                        names += str(re['name']) if 'name' in re else "None"
                        names += ' '
                    err += names
                    self._print_error_position('Error: dublicate!!!', err)
                    code = 422
                    raise Exception(err,code)
        



    def _check_bad_params(self,block):
        # INPUT
        # block is dict
        # fields:
        #   'name'
        #   'protocol'
        #   'port'
        #   'ip'
        #   'timeout'
        #   'proxies'
        #   'verify'
        #   'allow_redirects'
        #   'list_req'
        #       'location'
        #       'method'
        #       'data'
        #       'headers'
        #       'params'
        #       'posible_status_code'
        #       'expected_text'
        #       'expected_headers'
        #       'expected_status_code'
        #       'delay'
        #       'name'                  #uniq !!!! or generated!!!
        req_main = [ 'name','protocol','port','ip','timeout','proxies','verify','allow_redirects', 'list_req',]
        req_list_req = ['expected_status_code','location','method','data','headers','params','posible_status_code','expected_text','expected_headers','delay','name']

        
        for param in block:
            if not param in req_main:
#                print("BLOCK is:",block)
                err=  f"Error: Session got unexpected param: '{param}'."
                #self._print_error_position('missing reqired arg!!!',err)
                code = 422
                print(err)
                raise Exception(err,code)
#        print('block["list_req"]:',str(type(block['list_req'])),'\n\nlist:\t', block['list_req'])
        for dictionary in block['list_req']:
            for param in dictionary:
                if not param in req_list_req:
                    err= f"Error: Session got unexpected param: '{param}' in 'list_req'."
                    #self._print_error_position('missing reqired arg!!!',err)
                    print(err)
                    code = 422
                    raise Exception(err,code)











