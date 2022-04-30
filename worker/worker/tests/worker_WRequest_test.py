from worker.app.WReq import WRequest
from worker.variables import *
from worker.tests.create_yaml1 import *
from worker.tests.create_yaml2 import *
import pytest, requests, yaml, os, random


@pytest.mark.testclass
def test_init_without_params():
    try:
        req = WRequest()  # without params
        assert True
    except TypeError:
        print("Exception!")
        assert False
    except:
        print("Init problems")
        assert False


# test "instance" with wrong params
# we got doble delete when put incorect params
@pytest.mark.testclass
def test_init_WReqeust_instance_with_wrong_params():
    _list = [
        "aaa",
        3.14,
        1232131,
        {},
        [],
        True,
    ]
    for i in _list:
        try:
            my_instance = i
            # my_url = "http://wiki.org" # not requeired
            WRequest(
                instance=my_instance,
            )  # url=my_url)
            assert False
        except ValueError:
            assert True
        except:
            print("Big problems with instnce init")
            assert False


# test with right params
@pytest.mark.testclass
def test_init_WRequest_instance_with_right_params():
    try:
        #        my_prepped = Request('POST', url, data={"cool":"jacket"}, headers={"nice":"slippers"}).prepare
        my_instance = requests.Session()
        # my_url = test_server_url

        # init
        WRequest(
            instance=my_instance,
        )  # url=my_url)
    except:
        print("problems")
        assert False


@pytest.mark.slow
@pytest.mark.testclass
def test_init_with_right_other_params():
    # headers
    # proxies
    # method
    # url
    # data
    # params
    dict_of_list = {
        "headers": [  # headers
            {"123": "123"},
            {"sad": "not sad", "right": "wrong"},
            {
                "Content": "test",
            },
        ],
        "proxies": [  # proxies
            {
                "http": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
                "https": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
            },
        ],
        "method": [  # Type
            "GET",
            "POST",
            "PUT",
            "PATCH",  # We use eval and need string
        ],
        "url": [  # url
            "http://192.168.0.107",
            "http://192.168.0.107:67",
            "https://192.168.0.107",
            "https://192.168.0.107:45001",
            "http://google.com",
            "https://google.com",
        ],
        "data": [  # data
            {"123": "123"},
            {"sad": "not sad", "right": "wrong"},
            {
                "Content": "test",
            },
        ],
        "params": [  # params
            {"123": "123"},
            {"sad": "not sad", "right": "wrong"},
            {
                "Content": "test",
            },
        ],
    }
    # not needed random test
    # for i in range(75):
    #    try:
    #        wreq = _make_string_for_eval(dict_of_list)
    #        req = WRequest.__name__ +'('+ wreq+ ')'
    #        print(req)
    #        eval(req)
    #        assert True
    #    except ValueError:
    #        assert False
    for _dict in dict_of_list:

        for _item in dict_of_list[_dict]:
            try:
                if type(_item) == type(""):
                    _item = '"' + _item + '"'
                req = eval(
                    WRequest.__name__
                    + f"""( 
                    {_dict}={_item}
                    )"""
                )
                assert True
            except ValueError:
                # Not so bad
                assert False
            except:
                print("Init with expected values create error")
                assert False


@pytest.mark.testclass
def test_init_with_wrong_dict_params():
    # headers
    # proxies
    # url
    # method
    # params
    # data
    dict_of_list = {
        "headers": [  # headers
            {"123": 123},
            {123: "not sad", "right": None},
            {
                "Content": True,
            },
        ],
        "proxies": [  # proxies list(str)
            # {'http': f'{proxies_protocol}'},
            {"http": 123},
            {"http": None},
            # {'http': f'{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}'},
            # {'http': f'{proxies_protocol}'},
            {"http": True},
        ],
        "url": [
            "https://192.168.0",
            "htt://192.168.0.107:45001",
            "http:/google.com",
            # None, not here!!!
        ],
        "method": [  # Type
            "get",
            "POST1",
            "123",
            "True",  # We use eval and need string
        ],
        "params": [  # data
            {"123": 123},
            {123: "not sad", "right": None},
            {
                "Content": True,
            },
        ],
        "data": [  # headers
            {"123": 123},
            {123: "not sad", "right": None},
            {
                "Content": True,
            },
        ],
    }
    # for i in range(5_000_000):
    #    try:
    #        wreq = _make_string_for_eval(dict_of_list)
    #        req = WRequest.__name__ +'('+ wreq+ ')'
    #        print(req)
    #        eval(req)
    #        assert False
    #    except ValueError:
    #        assert True
    #    #except:
    #    #    assert False
    # 1 iten and 1 init
    for _dict in dict_of_list:

        for _item in dict_of_list[_dict]:
            try:
                if type(_item) == type(""):
                    _item = '"' + _item + '"'
                print(_dict, _item)
                req = (
                    WRequest.__name__
                    + f"""( 
                    {_dict}={_item}
                    )"""
                )
                print(req)
                eval(req)
                assert False
            except ValueError:
                # Not so bad
                assert True
            # except:
            #    print("Init with expected values create error")
            #    print(_dict,_item,)
            #    assert  False


def _make_string_for_eval(dict_of_list):  # Very usefull
    base = ""
    for _dict in dict_of_list:
        item = random.choice(dict_of_list[_dict])
        if type(item) == type(""):
            item = '"' + item + '"'  # to save string as strig before eval
        base += f"{_dict}={item}, "
    return base


@pytest.mark.testclass
def test_make_prepped():
    method = "GET"
    url = "http://test.me.com"
    headers = {"Content": "test_1"}
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
    print("test" + str(test))
    print("prepped" + str(prepped))

    assert instance.prepped.url == prepped.url
    assert instance.prepped.method == prepped.method
    assert instance.prepped.headers == prepped.headers


@pytest.mark.network
def test_send():
    url = test_server_url
    method = "GET"
    headers = {"Cook": "Duck"}

    req = WRequest(
        url=url,
        method=method,
        headers=headers,
    )
    answer = req.send()
    print(answer.status_code)
    assert answer.status_code == 200


@pytest.mark.network
def test_got_yaml():
    _file = "/yaml/WRequest_1.yaml"
    get_yaml_file(_file)  # from create_yaml1.py
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + _file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print("Data:", data)
        req = WRequest()
        req.set_proxies(data["proxies"])
        for request in data["list_req"]:  # test got_yaml(request)
            req.got_yaml(request)
            answer = req.send()
            assert answer.status_code == 200


@pytest.mark.network
def test_nginx_integrations():
    filename = "/yaml/WRequest_"
    pack(random=True, filename=filename)
    pack(random=False, filename=filename)
    path = os.path.dirname(os.path.realpath(__file__))

    # _yaml(path+'/yaml/WRequest_random.yaml')
    # We cant use it in our cause because we have some expected behavior from our server

    _yaml(path + "/yaml/WRequest_related.yaml")  # we take that exepected behavior


def _yaml(filename):  # 1) open yaml file
    # 2) make req
    # 3) check values
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print("Data:", data)
        req = WRequest()
        req.set_proxies(data["proxies"])
        for request in data["list_req"]:
            req.got_yaml(request)
            answer = req.send()

            # check data
            # assert answer.url == request['url'] # params change answer.url
            assert req.url == request["url"]
            if "params" in request:
                #            print("REQUEST:\t",request)
                #            req.get_status()
                #            print("DATA:\t",data)
                assert req.params == request["params"]
            if "headers" in request:
                assert req.headers == request["headers"]
            if "data" in request:
                assert req.data == request["data"]
            assert answer.ok
