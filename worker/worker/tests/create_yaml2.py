from worker.variables import *
import yaml, os
from varname import nameof
import random, uuid, copy

# 	Protocol	SSL	Port	Num
# 	http		no	80	    1
# 	https		yes	443	    2
# 	httpv2		yes	444	    3

# 	Location	Need	    	Answer	    	Used		Num
# 	/		    nothing	    	200,	    	1,2,3		1       #here
# 					            all files,
# 					            404
# 	/health		nothing	    	200		        1,2,3		2       #here
# 	/apikey		param: apikey	200,401	    	1,2,3		3       #here
# 	/redirect	nothing	    	301		        1.4->2.2	4
# 							                    2.4->2.2
# 							                    3.4->2.2
# 	/phealth	method: POST	200		        1,2,3		5
# 	/predirect1	method: POST	301		        1.6->2.5	6
# 							                    2.6->2.5
# 							                    3.6->2.5
# 	/papikey	method: POST	200,401	    	1,2,3		7
# 			    param: apikey
# 	/addheader	nothing 		200,	    	1,2,3		8
# 					            my_header value


def _add_proxies_randomly(instance):  # add randomly or not
    triger = random.choice([True, False])
    if triger:
        instance["proxies"] = {
            "http": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
            "https": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
        }

        print(instance["proxies"])
    else:
        instance["proxies"] = {}


def _get_name(prefix="test", name=None):  # uniq name
    if name:
        return name
    return prefix + "-" + str(uuid.uuid4())


def _get_dict_randomly():  # headers,params,data with random values
    rand_data = [
        "red",
        "yellow",
        "blue",
        "white",
        "black",
        "orange",
        "pink",
        "green",
        "grey",
        "brown",
    ]
    tmp = random.choice([True, False])
    if tmp:
        tmp = {}
        for i in range(random.randint(0, 3)):
            tmp[random.choice(rand_data)] = random.choice(rand_data)
        return tmp
    return None


def _get_method_randomly():
    return random.choice(["GET", "POST", None, "GET", None, None])


def _add_req(
    instance, url, name=None, method=None, headers=None, params=None, data=None
):
    if not "list_req" in instance:
        instance["list_req"] = []

    # create dict which we will add
    tmp = {}
    tmp[nameof(url)] = url
    if name:
        tmp[nameof(name)] = name
    if method:
        tmp[nameof(method)] = method
    if headers:
        tmp[nameof(headers)] = headers
    if params:
        tmp[nameof(params)] = params
    if data:
        tmp[nameof(data)] = data
    print(tmp)
    instance["list_req"].append(tmp)


def get_yaml_data_related(table):  # related to test_server_url_table
    # l_sessions = []
    item = table
    locations = item["list_req"]
    session = {}
    session["name"] = _get_name("session")
    session["proxies"] = item["proxies"]
    for location in locations:
        url = f"""{item["protocol"]}://{test_server_ip}{item["port"]}{location["location"]}"""
        print("+" * 23)
        print("LOCATION", location)
        _add_req(
            instance=session,
            url=url,
            method=location["method"],
            name=_get_name("req", location["name"]),  # random req name
            headers=copy.deepcopy(location["headers"]),
            data=copy.deepcopy(location["data"]),
            params=copy.deepcopy(location["params"]),
        )
    print("-" * 23)
    print("SESSION", session)
    print("-" * 23)
    return session


#   l_sessions.append(session)

# return l_sessions # return right created obj
def pack(random=False, filename="WRequest_"):
    if random:
        data = get_yaml_data_randomly()
        postfix = "random.yaml"
    else:
        data = get_yaml_data_related(test_server_url_table)
        postfix = "related.yaml"
    get_yaml_file2(filename=filename + postfix, data=data)


def get_yaml_data_randomly():
    session = {}
    _add_proxies_randomly(session)
    session["name"] = _get_name("session")
    _add_req(
        instance=session,
        url=test_server_url,
        method=_get_method_randomly(),
        name=_get_name("req"),
        headers=_get_dict_randomly(),
        data=_get_dict_randomly(),
        params=_get_dict_randomly(),
    )
    return session


# Dynamic yaml
def get_yaml_file2(filename, data):
    # data = get_session_data()
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + "/" + filename, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
        print("done", path)
