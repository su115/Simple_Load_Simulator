from worker.app.WReq import WRequest
from worker.app.CReq import CRequest
from worker.variables import *
import pytest, uuid

@pytest.mark.testclass
def test_CRequest_init():
    try:
        posible_status_code= [200, 404]# None = any
        expected_status_code= 200 # None = any
        expected_text= "health"   # None = any
        expected_headers= None
        salt=str(uuid.uuid4())[:6]
        name="session-creq-"+salt   


        CRequest(
        name=name,
        salt=salt,
        posible_status_code=posible_status_code,
        expected_status_code=expected_status_code, 
        expected_text=expected_text,
        expected_headers=expected_headers,
        )
    except:
        assert False
