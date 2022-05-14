from flask import Flask, request,  jsonify, Response
from worker.app.WSession import WSession
from waitress import serve
import os, requests, json, time, logging 
def now():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return str(current_time)



logging.basicConfig(filename='/var/log/sls_worker.log', encoding='utf-8', level=logging.DEBUG)

MASTER_IP = os.environ.get("MASTER_IP")
MASTER_PORT = os.environ.get("MASTER_PORT")
POD_IP = os.environ.get("POD_IP")
POD_NAME = os.environ.get("POD_NAME")
NAMESPACE = os.environ.get("NAMESPACE")
POD_PORT = os.environ.get("POD_PORT")
if (
    MASTER_IP == None
    or POD_IP == None
    or POD_NAME == None
    or NAMESPACE == None
    or POD_PORT == None
    or MASTER_PORT == None
):
    t = now()
    info = f"[{t}] Some args is missing, Cancel worker registration!!! MASTER_IP: {MASTER_IP}, MASTER_PORT: {MASTER_PORT}  POD_NAME: {POD_NAME},  POD_IP: {POD_IP},  NAMESPACE: {NAMESPACE},  POD_PORT: {POD_PORT}; "
    print(info)
    logging.error(info)
    raise Exception( info )
    

app = Flask(__name__)


#
#   REGISTER CODE
#
def register_worker():  # register to master
    #print('register_worker()')
    headers = {"Content-Type": "application/json"}
    block = {}
    block["pod_name"] = POD_NAME
    block["namespace"] = NAMESPACE
    block["pod_ip"] = POD_IP
    block["pod_port"] = POD_PORT
    url = f"http://{MASTER_IP}:{MASTER_PORT}/register_worker"
    json_data = json.dumps(block)
    try:
        req = requests.post(headers=headers, url=url, data=json_data)
    except requests.exceptions.ConnectionError:
        t = now()        
        info = f"[{t}] ConnectionError: can't connect to master. url: {url}"
        print(info)
        logging.info(info)        
        return False
    else:
        if req.status_code == 200:
            if req.text == "registred":
                t = now()
                info = f"[{t}] Worker registred : {POD_NAME}, {POD_IP}:{POD_PORT} in {NAMESPACE} namespace."
                print(info)
                logging.info(info)
                return True
            else:
                t = now()
                info=f"[{t}] Register error: {req.text}."
                print(info)
                logging.error(info)
        else:
            t = now()
            info= f"[{t}] Master is unavailible: answer_status_code: {req.status_code} {req.text}"
            print(info)
            logging.error(info)
        return False


@app.route("/worker", methods=["POST"])
def post_data():
    err = "Error: worker->main.py post_data: "
    block = request.json

    try:
        wses = WSession(block)
        #wses.is_valid(block)
        wses.send()
    except Exception as e:
#        print(f'/worker got problems!!! args: {e.args}')
        t = now()
        info =f'[{t}] ' + err + f"Exception: {e}"
        print(info)
        logging.error(info)
        return  jsonify(e.args[0]), e.args[1]
    #    print("/worker works fine")
    return jsonify(wses.list_resaults)


@app.route("/is_valid_block", methods=["POST"])
def is_valid():
    err = "Error: worker->main.py is_valid: "
    block = request.json
    try:
#        print('before WSession init')
        wses = WSession(block)
        wses.is_valid(block)
#        print('after WSession init')
    except Exception as e:
 #       print(f"/worker say isn't valid: {e.args}")
        t = now()
        info =f'[{t}] ' + err + f"Exception: {e}"
        print(info)
        logging.error(info)       
        return jsonify(e.args[0]), e.args[1] #check please
#    print('/worker say is valid')
    return "valid"


@app.route("/healthz", methods=["GET"])  # check if server works
def healthz():
    #    print("I'm healthz!!!")
    return "healthz"


if __name__ == "__main__":
    while not register_worker():
        time.sleep(5)
#    schedule.every(1).minutes.do(register_worker)
#    schedule.run_pending()
    # app.run(host='localhost', port=7799,debug=True) # Debug
    serve(app, port=POD_PORT)
