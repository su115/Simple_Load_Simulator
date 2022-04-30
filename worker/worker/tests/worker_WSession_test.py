from worker.app.WReq import WRequest
from worker.app.CReq import CRequest
from worker.app.WSession import WSession
from worker.variables import *
import uuid, pytest

# test init
@pytest.mark.testclass
def test_WSession_init_with_params():
    block = test_server_url_table
    try:
        wses = WSession(block)
        assert True
    except:
        assert False

# test send 1
@pytest.mark.network
def test_WSessiopn_send():
    block = test_server_url_table
    try:
        wses = WSession(block)
        wses.send()
        for req in wses.list_resaults: # list of resaults
            print('req:',req['error'])
            assert not req['error'] # req['error'] = []
        assert True
    except:
        assert False
# test send 2
@pytest.mark.network
def test_WSession_send2():
    block = test_server_url_table2
    try:
        wses = WSession(block)
        wses.send()
        for req in wses.list_resaults: # list of resaults
            print('req:',req['error'])
            assert not req['error'] # req['error'] = []
        assert True
    except:
        assert False
# test send 3
@pytest.mark.network
def test_WSession_send2():
    block = test_server_url_table3
    try:
        wses = WSession(block)
        wses.send()
        for req in wses.list_resaults: # list of resaults
            print('req:',req['error'])
            assert not req['error'] # req['error'] = []
        assert True
    except:
        assert False
