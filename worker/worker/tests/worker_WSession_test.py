from worker.app.WReq import WRequest
from worker.app.CReq import CRequest
from worker.app.WSession import WSession
from worker.variables import *
import uuid, pytest, copy

# test init
@pytest.mark.testclass
def test_WSession_init_with_params():
    block = test_server_url_table.copy()
    try:
        wses = WSession(block)
        assert True
    except:
        assert False
# test init without some params
@pytest.mark.testclass
def test_WSession_init_without_some_params():
    block = copy.deepcopy(test_server_url_table)
    required_main = ['name','ip', 'list_req']
    required_list_req = ['expected_status_code','location']
    for key in required_main:
        try:
            tmp_block = block.copy()
            del tmp_block[key]
            wses = WSession(tmp_block)
            assert False
        except:
            assert True
    tmp_block = block.copy()
    for key in required_list_req:
        del tmp_block['list_req'][0][key]
        try:
            WSession(tmp_block)
            assert False
        except:
            assert True    
        
            
            
# test send 1
@pytest.mark.network
def test_WSessiopn_send1():
    block = test_server_url_table.copy()
    try:
        wses = WSession(block)
        wses.send()
        for req in wses.list_resaults: # list of resaults
            #print('req:',req['error'])
            assert not req['error'] # req['error'] = []
        assert True
    except:
        assert False
# test send 2
@pytest.mark.network
def test_WSession_send2():
    block = test_server_url_table2.copy()
    try:
        wses = WSession(block)
        wses.send()
        for req in wses.list_resaults: # list of resaults
            #print('req:',req['error'])
            assert not req['error'] # req['error'] = []
        assert True
    except:
        assert False
# test send 3
@pytest.mark.network
def test_WSession_send3():
    block = test_server_url_table3.copy()
    try:
        wses = WSession(block)
        wses.send()
        for req in wses.list_resaults: # list of resaults
#            print('req:',req['error'])
            assert not req['error'] # req['error'] = []
        assert True
    except:
        assert False

# test send 4 requests.exceptions.ConnectionError
@pytest.mark.testclass
def test_WSession_send1_ConnectionError():
    block = test_server_url_table.copy()
    block['list_req'] = []
    block['list_req'].append(test_server_url_table['list_req'][0])
    
    block['ip'] = 'llll.oew'
    print('Block before test',block)
    try:
        wses = WSession(block)
        wses.send()
        for req in wses.list_resaults: # list of resaults
            #print('req:',req)
            if isinstance(req,str):
                continue
            if not req['error']: # req['error'] != []
                assert False
            else:
                err = 'ConnectionError'
                if not err in req['error'][0]: # HARD LOCK HERE!!!!
                    assert False
        assert True
    except:
        #print("block:",block)
        assert False
