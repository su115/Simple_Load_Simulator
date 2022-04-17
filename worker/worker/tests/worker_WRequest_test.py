from worker.app.main import WRequest
from worker.variables import *
from worker.tests.create_yaml1 import *
from worker.tests.create_yaml2 import *
import pytest, requests, yaml, os

@pytest.mark.testclass
def test_init_without_params():
    try:
        req = WRequest() #without params
        assert True 
    except TypeError:
        print("Exception!")
        assert False

@pytest.mark.testclass
def test_init_with_wrong_params():
        _list = [
                "aaa",
                3.14,
                1232131,
                True,
                ] 
        for i in _list:
            try:
                my_instance = i
                my_url = "http://wiki.org"
                WRequest(instance=my_instance, url=my_url)
                assert False
            except ValueError:
                assert True
            except:
                assert False


@pytest.mark.testclass
def test_init_with_right_params():
    try:
        my_instance = requests.Session()
                      
        my_url = "http://wiki.org"
        WRequest(instance=my_instance, url=my_url)
    except:
        assert False 


@pytest.mark.testclass
def test_init_with_right_dict_params():
    dict_of_list = {
            "headers":[#headers 
                {"123":"123"},
                {"sad":"not sad","right":"wrong"},
                {"Content":"test",}
            ],
            "proxies":[#proxies
                
                    {
                        'http': f'{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}',
                        'https': f'{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}',
                    },     
                
            ],
            "method":[#Type
                "\"GET\"",
                "\"POST\"",
                "\"PUT\"",
                "\"PATCH\"",# We use eval and need string
                ],
            "url":[#url
                "\'http://192.168.0.107\'",
                "'http://192.168.0.107:67'",
                "'https://192.168.0.107'",
                '"https://192.168.0.107:45001"',
                "\"http://google.com\"",
                "\"https://google.com\"",
                ],
            "data":[#data
                {"123":"123"},
                {"sad":"not sad","right":"wrong"},
                {"Content":"test",}               
                ],
            "params":[#params
                {"123":"123"},
                {"sad":"not sad","right":"wrong"},
                {"Content":"test",}               
                ],


    }
    instance = requests.Session()
    for _dict in dict_of_list:
        
        for _item in dict_of_list[_dict]:
            try:
                print(_dict,_item)
                req = eval( WRequest.__name__+ f"""( 
                    instance=None,
                    {_dict}={_item}
                    )""")
                assert True 
            except ValueError:
                assert False
            except:
                print("Init with expected values create error")
                assert False


@pytest.mark.testclass
def test_init_with_wrong_dict_params():
    dict_of_list = {
            "headers":[#headers 
                {"123":123},
                { 123:"not sad","right": None},
                {"Content": True,}
            ],
            "proxies":[#proxies list(str)
                
                    {'http': f'{proxies_protocol}'},
                    {'http': "\"123\""},
                    {'http': "None"},
                    {'http': f'{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}'},
                    {'http': f'{proxies_protocol}'},
                    {"http": "True"},                    
                
            ],
            "method":[#Type
                "\'get\'",
                "\"POST1\"",
                "123",
                "True",# We use eval and need string
                ],

            "params":[#data 
                {"123":123},
                { 123:"not sad","right": None},
                {"Content": True,}
            ],
            "data":[#headers 
                {"123":123},
                { 123:"not sad","right": None},
                {"Content": True,}
            ],
    }
    for _dict in dict_of_list:
        
        for _item in dict_of_list[_dict]:
            try:
                req = eval( WRequest.__name__+ f"""( 
                    instance=\'None\',
                    url=\'None\',
                    {_dict}={_item}
                    )""")
                assert  False
            except ValueError:
                # Not so bad
                assert  True
            except:
                print("Init with expected values create error")
                assert  False
 
@pytest.mark.testclass
def test_make_prepped():
    method = "GET"
    url = "http://test.me.com"
    headers = {"Content":"test_1"}
    req = requests.Request(
            method=method,
            url=url,
            headers=headers,
            )
    prepped = req.prepare()
    instance = WRequest(
            url=url,
            method=method,
            headers=headers,
            )
    test = instance._make_prepped()
    print("test"+str(test))
    print("prepped"+str(prepped))

    assert instance.prepped.url == prepped.url
    assert instance.prepped.method == prepped.method
    assert instance.prepped.headers == prepped.headers
@pytest.mark.testclass
def test_send():
    url = test_server_url
    method = "GET"
    headers = {"Cook":"Duck"}
    req = WRequest(
            url=url,
            method=method,
            headers=headers,
            )
    answer = req.send()
    print(answer.status_code)
    assert answer.status_code == 200
@pytest.mark.testclass
def test_got_yaml():
    get_yaml_file() #from create_yaml1.py
    path = os.path.dirname(os.path.realpath(__file__))
    with open( path+'/WRequest_1.yaml') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        print("Data:",data)
        req = WRequest()
        req.set_proxies(data['proxies'])
        for request in data['list_req']:
            req.got_yaml(request)
            answer = req.send()
            assert answer.status_code == 200
@pytest.mark.testclass
@pytest.mark.integration
def test_nginx_integrations():
    pack(random=True)
    pack(random=False)
    path = os.path.dirname(os.path.realpath(__file__))

   # _yaml(path+'/WRequest_random.yaml')
    _yaml(path+'/WRequest_related.yaml')

def _yaml(filename):
    with open( filename ) as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        print("Data:",data)
        req = WRequest()
        req.set_proxies(data['proxies'])
        for request in data['list_req']:
            req.got_yaml(request)
            answer = req.send()

            # check data
            #assert answer.url == request['url'] # params change answer.url
            assert req.url == request['url']
            if 'params' in request:
#            print("REQUEST:\t",request)
#            req.get_status()
#            print("DATA:\t",data)
                 assert req.params == request['params']
            if 'headers' in request:
                assert req.headers == request['headers']
            if 'data' in request:
                assert req.data == request['data']
            assert answer.ok
