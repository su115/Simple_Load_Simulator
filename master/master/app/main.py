from flask import Flask, request, jsonify, Response
from master.app.Worker import Worker # we w
from master.app.Simulation import Simulation
from waitress import serve
import json
import time, logging

# try detached
#from multiprocessing import Manager 
#time_list = Manager.list()


logging.basicConfig(filename='/var/log/sls_master.log', encoding='utf-8', level=logging.DEBUG )
app = Flask(__name__)
worker_list = []
dashboard = [] #Manager().list()    # Dangerous
                                # all processes have access to list

def now():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return str(current_time)

@app.route('/ongoing',methods=['GET'])
def ongoing_work():
    err = 'Error: master->main.py ongoing_work: '
                        # INPUT  { simulation_name:   [ time_stamp, count_ok, count_notok ] } # EXPECTED 
                        # OUTPUT { simulation_name: [ [ time_stamp, count_ok, count_notok ] ] } #sorted to 1 timestamp per 10 sec
    #   REALITY
    #[ <-- dashboard
    #   
    #   { <-- simulation_dict
    #       'Simulation-2' <-- simulation_name   : [ <-- simulation_dict
    #           ['03:04:15', 1, 1], <-- timestamp
    #       ]
    #   }, 
    #   {'Simulation-1': [['03:04:23', 1, 1], ['03:04:27', 1, 1]]}
    #]
    print("="*20)
    print("before_dashboard:",dashboard)
    for simulation_dict in dashboard: # calculate count  [ "01:12:46"] --> [::-1][1::] '4:21:10'
        print('\tsimulation_dict:',simulation_dict)
        for simulation_name in simulation_dict:
                print('\t'*2+'simulation_name: ',simulation_name)
                dump = []
                for  timestamp in simulation_dict[simulation_name]:
                    print('\t'*3+'timestamp: ',timestamp)
                    if not dump: #empty
                        dump.append( timestamp )
                        print('\t'*4+'add first timestamp: ',timestamp)
                        continue
                    notequal = True
                    for dtimestamp in dump: # must be not empty
                        if timestamp[0][:-1] == dtimestamp[0][:-1]: # equal
                            print('\t'*5+'equal  timestamp: ',timestamp,  "\trev: ",timestamp[0][:-1], dtimestamp[0][:-1])
                            dtimestamp[1] += timestamp[1] #is ok
                            dtimestamp[2] += timestamp[2] #not ok
                            
                            dtimestamp[0] = timestamp[0][:-1]+'0' #'0'+timestamp[0][::-1][1::] # to 0
#                            dtimestamp[0] = dtimestamp[0][::-1]
                            notequal = False
                    if notequal:
                        print('\t'*5+'notequ timestamp: ',timestamp, "\trev: ",timestamp[0][::-1][1::], timestamp[0][::-1][1::])
                        l = [] # to 0
                        t = timestamp[0][:-1] + '0'  #'0'+timestamp[0][::-1][1::]
                        #t = t[::-1] # reverse
                        l.append(t)
                        l.append(timestamp[1])
                        l.append(timestamp[2])
                        dump.append( l )
                simulation_dict[simulation_name] = dump

                        
    print("after_dashboard: ",dashboard)
    print('='*20)
#    dashboard.clear()
    tmp = list(dashboard)
    return jsonify(tmp),200
@app.route('/ongoing/clear',methods=['GET'])
def clear_dashboard():
    dashboard[:]=[]
    return "cleaned"

@app.route('/master',methods=['POST'])
def post_data():
    err = 'Error: master-->main.py post_data: '
    
    simulation = request.json
    #return 200    
    try:
        #print("worker_list:",worker_list)
        #print("Simulation:",simulation)
        sim = Simulation(simulation,worker_list)
        resaults = sim.start( dashboard )
#        print(resaults) 
    except Exception as e:
        t = now()
        info = f'[{t}] '+err+ str(e)
        print(info)
        logging.error(info)
        #print(jsonify(str(e)),str(400))
        return  Response(info,status=400)
#    print('before error') 
    return  jsonify(resaults),200

#@app.route('/master/detached',methods['POST'])
#def post_data_detached():
#    err = 'Error: master-->main.py post_data_detached: '
#    try:
#        simulation = request.json
        

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



@app.route('/healthz',methods=['GET']) # check if server works
def healthz():
    return 'healthz'

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=7790,debug=True) # Debug
    serve(app,port=7790)
