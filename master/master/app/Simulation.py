from  master.app.Worker import Worker
import random, copy, uuid
import multiprocessing

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
            
        
    def start(self): # start work
        err = 'Error: Simulation: start: '
        if not ( self.threads >= 1 and  self.threads <= 10):
            raise Exception(err+f"parameter 'threads' out of the range. must be 1 <= 'threads' <= 10, but it was {self.threads}.")
        resaults = []
#        print("start simulation: ",self.name)
        procs = []
        

        def _proc(job,resa,worker,msg):
            for i in range(self.repeat):
                 tmp_session = copy.deepcopy(self.session)
                 if 'name' in self.session:
                     tmp_session['name'] = self.session['name'] + '-threads-'+str(job)+ f'-repeat-{i + 1}'
                 else:
                    tmp_session['name'] = 'Session-'+str( uuid.uuid4() )[:8] + '-threads-'+str(job)+ f'-repeat-{i+1}'
                 #worker = random.choice(self.workers)
                 
                 resa.append( worker.work(tmp_session) )
#                 print(msg) #debug only

        with multiprocessing.Manager() as manager:
                L = manager.list()  # <-- can be shared between processes.                
                for job in range(self.threads ):
                    num =  job+1
                    worker = random.choice(self.workers)
                    msg = "Work:"+str(job+1)+'/'+str(self.threads)+f' {worker.pod_name}' 
                    p = multiprocessing.Process(target=_proc,args=(num,L,worker,msg))
                    #_proc(job+1)     
                    procs.append(p)
                    p.start()
    
                for proc in procs:
                    proc.join()
                resaults = list(L)
        resaults.append(self.name) # add name of Simulation
        return resaults

