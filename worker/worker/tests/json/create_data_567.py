#! /bin/python3
from worker.variables import *
import json
import os
filedata = {
    "data5.json": test_server_url_table,
    "data6.json": test_server_url_table2,
    "data7.json": test_server_url_table3,
}
path = os.path.dirname( os.path.realpath(__file__) )

for key in filedata:
    with open(path +'/' + key, 'w') as f:
        print(path+'/'+key)
        #print(filedata[key])
        f.write( json.dumps(filedata[key], sort_keys=True, indent=4) ) 
