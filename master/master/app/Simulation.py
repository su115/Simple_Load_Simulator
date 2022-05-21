from  master.app.Worker import Worker
import random, copy, uuid, time
import multiprocessing
from master.app.Report import Timestamp, Timereport
from multiprocessing.managers import BaseProxy
from multiprocessing.dummy import Pool


class Simulation:
    def __init__(self, 
                 block,
                 workers,  # Never empty !!!!!
                ) -> None:
        # repeat
        # name  #Generated
        # session
        # threads
        

        err = "Error: Simulation: __init__: "
        self._check_bad_params(block)
        # NAME
        if "name" in block:
            if isinstance(block['name'] , str):
                self.name   = block['name']
            else:
                raise Exception(err +"parameter 'name' isn't type 'str'.")       # str
        else:
            self.name = "Simulation-"+str( uuid.uuid4() )[:8]
            #raise Exception(err + "parameter 'name' isn't exists.")

        # REPEAT
        if 'repeat' in block:
               if isinstance(block['repeat'],int):
                    if block['repeat'] >= 1 and block['repeat'] <= 100:
                        self.repeat = block['repeat']
                    else:
                        raise Exception(err + "parameter 'repeat' isn't in diapasone 1 <= 'repeat' <= 100.")    # int
               else:
                    raise Exception(err + "parameter 'repeat' isn't type 'int'.")    # int
        else:
                self.repeat = 1
#            raise Exception(err+"parameter 'repeat' isn't exists.")

        # WORKERS
        self._set_workers(workers)

        # SESSION
        w = random.choice(self.workers)
        if 'session' in block:
 #           print("Block:",block["session"])
            if w.is_valid( block['session'] ):
    
                self.session = block["session"]
#                print("IS VALID")
            else:
                raise Exception(err+"'block['session']' failed validation!")

        else:
            raise Exception(err+"parameter 'session' isn't exists.")

        # threads
        if 'threads' in block:
             if isinstance(block['threads'],int):
                if block['threads'] >= 1 and block['threads'] <= 10:
                    self.threads = block['threads'] 
                else:
                    raise Exception(err + "parameter 'threads' isn't in diapasone 1 <= 'threads' <= 10.")    # int
             else:
                 raise Exception(err + "parameter 'threads' isn't type 'int'.")    # int
        else:
            self.threads = 1
#            raise Exception(err+"parameter 'threads' isn't exists.")

        # detached
        if 'detached' in block:
            if isinstance( block['detached'],bool ): # when you use detached 
                                                     # you must be sure that "session": 
                                                     #                          "list_req":
                                                     #                              "delay": 0.1, <-- is at list 0.1
                #print("check detached 1")
                if 'list_req' in  self.session:
                    
                    for req in self.session['list_req']:
                        if not 'delay' in req:
                            raise Exception(err +" 'detached' is used but 'session'->'list_req'->'delay' is not used in every req.")
                        else:
                            if req['delay'] >= 0.1 and req['delay'] <= 15.0:
                                pass # match all expression
                            else:
                                raise Exception(err +" 'detached' is used but 'session'->'list_req'->'delay' is not in diapazone: 0.1 <= 'delay' <= 15.0 ")
                else:
                    raise Exception(err +" 'detached' is used but 'session'->'list_req' isn't exists.")
                self.detached = block['detached']
            else:
                self.detached = False
                raise Exception(err + "parameter 'detached' isn't type 'bool'.")
        else:
            self.detached = False 

    def _set_workers(self,workers):
        err = "Error: Simulation: set_workers: "
        self.workers = [] # clean workers list
        unavailible_workers = ''
        if workers: # if empty we dont change
            for w in workers:
                if isinstance(w,Worker):
                    if w.is_healthz():    # is health
                        if not  w in self.workers: # not already here
                            self.workers.append( w)
                    else:
                        uw = f"Worker: {w.pod_name} is unavailible."
                        unavailible_workers += uw + '\n'
                    
                        print(uw)
                else:
                    raise Exception(err+"you put list with not Worker instances.")
        else:
            raise Exception(err+ "Worker list is empty!!! None of registred worker!!!")
        if not  self.workers: # if empty !!!!
            raise Exception(err+ "Worker list is empty!!! None of registred worker!!!\n"+unavailible_workers)
            
    # _check_bad_params
    def _check_bad_params(self,block):
    #   'name'
    #   'session'
    #   'threads'
    #   'repeat'
    #   'detached'
        sim_params = ['name','session','threads','repeat','detached']    
        for param in block:
            if not param in sim_params:
                err= f"Error: Simulation got unexpected param: '{param}'."
#                logging.error(err)
#                print(err)
                raise Exception(err)
############################################# START ##############################################
    def _proc(  self,
                job,
                resa,
                worker,
                msg,
                time_l,
                ):
            def timed():
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    return str(current_time)
            for i in range(self.repeat):
                 tmp_session = copy.deepcopy(self.session)
                 if 'name' in self.session:
                     tmp_session['name'] = self.session['name'] + '-threads-'+str(job)+ f'-repeat-{i + 1}'
                 else:
                    tmp_session['name'] = 'Session-'+str( uuid.uuid4() )[:8] + '-threads-'+str(job)+ f'-repeat-{i+1}'
                 resault  = worker.work(tmp_session) # work !!!!
                 is_ok = 0
                 not_ok = 0
                 #[
                 #   "Session-319ade9a",
                 #    {
                 #     "error":["expected_status_code: 200 answer_status_code: 301"],
                 #     "name":"Session-319ade9a-request-496806"
                 #    }
                 #]
                 for req in resault:
                    if isinstance(req,str): # skip Session-319ade9a
                        continue
                    if req['error']: #empty
                        is_ok += 1
                    else:
                        not_ok+= 1
                 resa.append( resault ) # We need take count OK and NOTOK
                 time_l.append(  Timereport( name=tmp_session['name'],l_timestamps= [Timestamp(timed(), is_ok, not_ok) ]  )) 


    def start(self,T ): # start work
        err = 'Error: Simulation: start: '
        if not isinstance(T, BaseProxy):
            raise Exception(err+ " param 'T' is not type 'list'.") 
        resaults = []
        procs = []
        with multiprocessing.Manager() as manager:
                L = manager.list()  # <-- can be shared between processes.
                time_list = manager.list()   # timestamps 
                if  self.detached:
                    pool = Pool( self.threads ) # <-- !!!!!
                    l_p = []
                for job in range(self.threads ):
                    num =  job+1
                    worker = random.choice(self.workers)
                    msg = "Work:"+str(job+1)+'/'+str(self.threads)+f' {worker.pod_name}' 
                    
                    if self.detached:
                        pool.apply_async(self._proc, args=(num,L,worker,msg,T)) 
                    else:
                        p = multiprocessing.Process(target=self._proc,args=(num,L,worker,msg,T))
                        procs.append(p)
                        p.start()
                if self.detached:
                    return False
                #if not self.detached:
                for proc in procs:
                    proc.join()
                resaults = list(L)

        resaults.append(self.name) # add name of Simulation
        
        return resaults

