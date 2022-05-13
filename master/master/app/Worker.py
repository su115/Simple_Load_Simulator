import requests, json

class Worker:
    def __init__(self, pod_name: str, pod_ip: str, namespace: str, worker_port: int ) -> None:
        self.pod_name = pod_name
        self.pod_ip = pod_ip
        self.namespace = namespace
        self.port = worker_port

    def is_healthz(self):
        url = f'http://{self.pod_ip}:{self.port}/healthz'
#        print("URL:\t",url)
        req = requests.get(url=url)
        if req.status_code == 200:
            if  req.text == 'healthz':
               return True
        return False

    def work(self,session):
        err = "Error: Worker: work: " 
        url = f'http://{self.pod_ip}:{self.port}/worker'
        headers = {"Content-Type": "application/json"}
        json_block = json.dumps(session)
        req = requests.post(url=url,headers=headers,data=json_block)
        if req.status_code == 200:
            return json.loads(req.text)
        else:
            raise Exception(err + f"answer status_code: {req.status_code}    answer text:{req.text}")
    def is_valid(self,block):
        err = "Error: Worker: is_valid: " 
        url = f'http://{self.pod_ip}:{self.port}/is_valid_block'
        headers = {"Content-Type": "application/json"}
        json_block = json.dumps(block)
        req = requests.post(url=url,headers=headers,data=json_block)
        if req.status_code == 200:
#            if req.text == "not valid":
#                return False
            if req.text == "valid":
                return True
            raise Exception(err + f"got unexpected answer {req.text}")
        raise Exception(err + f"answer status_code: {req.status_code}    answer text:{req.text}")

    def __eq__(self,other):
        if self.pod_ip == other.pod_ip and self.pod_name == other.pod_name:
            return True
        return False
