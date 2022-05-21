from flask import Flask, request, jsonify, Response
from master.app.Worker import Worker # we w
from master.app.Simulation import Simulation
from waitress import serve
import json
import time, logging

# try detached
from multiprocessing import Manager 
#time_list = Manager.list()


logging.basicConfig(filename='/var/log/sls_master.log', encoding='utf-8', level=logging.DEBUG )
app = Flask(__name__)
worker_list = []
dashboard = Manager().list()    # Dangerous
                                # all processes have access to list

def now():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return str(current_time)

@app.route('/ongoing',methods=['GET'])
def ongoing_work():
    err = 'Error: master->main.py ongoing_work: '
    tmp = [] 
    for timereport in dashboard:
        tmp.append( timereport.simple() )
    return jsonify(tmp),200

@app.route('/ongoing/clear',methods=['GET'])
def clear_dashboard():
    dashboard[:]=[]
    return "cleaned"

@app.route("/healthz", methods=["GET"])  # check if server works
def healthz():
    #    print("I'm healthz!!!")
    return "healthz"

@app.route('/master',methods=['POST'])
def post_data():
    err = 'Error: master-->main.py post_data: '
    
    simulation = request.json
    try:
        sim = Simulation(simulation,worker_list)
        resaults = sim.start( dashboard )
    except Exception as e:
        t = now()
        info = f'[{t}] '+err+ str(e)
        print(info)
        logging.error(info)
        return  Response(info,status=400)
    return  jsonify(resaults),200

@app.route('/validate',methods=['POST'])
def validate():
    err = "Error: master-->main.py validate: "
    try:
        data = request.json
        sim = Simulation(data,worker_list)
    except Exception as e:
        t = now()
        info = f"[{t}] {err} Validation failed: {e}" 
        print(info)
        logging.error(info)
        return Response('Validation failed: '+str(e),status=422)
    return "valid"

@app.route('/register_worker',methods=['POST'])
def register_worker():
    block = request.json
    try:
        #print(block) 
        worker = Worker(
                block['pod_name'],
                block['pod_ip'],
                block['namespace'],
                block['pod_port']
                )  # validate json in paralel
        if worker.pod_ip:
            tmp = True
            t = now()
            if worker in worker_list:
                info = f"[{t}] Worker is alredy registred!!!"
                print(info)
                logging.info(info)
            else:
                worker_list.append(worker)
                info = f"[{t}] Registred new worker: {worker.pod_name}, {worker.pod_ip}:{worker.port}, in {worker.namespace} namespace."
                print(info)
                logging.info(info)
    except Exception as e:
        t = now()
        info = f"[{t}] Failed promt to register new worker!!!!" + str(e.args[0])
        print(info)
        logging.error(info)
        return 'not registred'
    return 'registred'



if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=7790,debug=True) # Debug
    serve(app,port=7790)
