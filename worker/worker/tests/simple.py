from worker.app.main import *
import yaml
f = open('/home/clone9/flask/core/Simple_Load_Simulator/worker/worker/tests/WRequest_related.yaml')
data = yaml.load(f,Loader=yaml.FullLoader)
req = WRequest()
print(data['list_req'][1])
req.got_yaml(data['list_req'][1])
req.get_status()
answer = req.send()
print(str(answer.status_code))





