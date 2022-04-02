from worker.app.main import WRequest
import pytest

@pytest.mark.testclass
def test_init_without_params():
    try:
        req = WRequest() #without params
    except:
        print("Got Exception!")
        assert False == True
    assert req.headers == None

@pytest.mark.testclass
def test_init_with_right_header_params():
    header_list = [ 
            {"123":"123"},
            {"sad":"not sad","right":"wrong"},
            {"Content":"test",}
            ]
    for header in header_list:
        try:
            print(header)
            req = WRequest(header)
            assert req.headers== header
        except:
            print("Init with expected values create error")
            assert True == False
               
@pytest.mark.testclass
def test_init_with_wrong_header_params():
    header_list = [ 
            {"123":123},
            {"sad":"not sad","right":34.3},
            ]
    for header in header_list:
        try:
            req = WRequest(header)
            #assert req.header == header
        except ValueError:
            assert True == True
        except:
            print("Init with unexpected values create enexpected error")
            assert True == False
 
