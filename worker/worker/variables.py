# Proxy
proxies_user = "your_dante_user"
proxies_pass = "EvanescaPassworsd1sr5"
proxies_ip = "ec2-13-53-212-77.eu-north-1.compute.amazonaws.com"
#'ec2-13-51-194-209.eu-north-1.compute.amazonaws.com'
# "ec2-13-51-201-196.eu-north-1.compute.amazonaws.com"
proxies_port = "45001"
proxies_protocol = "socks5"

# Server

test_server_params = {
    "apikey": "4420d1918bbcf7686defdf9560b"
}  # Sometimes to some links

test_server_url = f"http://{proxies_ip}"  # Main url
test_server_ip = f"{proxies_ip}"
test_server_url_table = {
    "name": "WSession-1",# None = any
    "port": ":80",
    "protocol": "http",  # http or https
                         # httpv2 -> https
    
    "ip": proxies_ip,
    "allow_redirects": True,
    "proxies": {
        "http": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
        "https": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
    },
    "timeout": (1, 5),# timeout of Request
    "verify": False,
    "list_req": [
        {
            "location": "/",
            "name": None,
            "headers": None,
            "params": None,
            "data": None,
            "method": "GET",# None = GET
            "posible_status_code": [200, 404],# None = any
            "expected_status_code": 200,# None = any
            "expected_text": None, # "health",  # None = any
            "expected_headers": None,
            "delay":2.1 , # delay after request
        },  # Done
        {
            "location": "/health",
            "headers": None,
            "params": None,
            "data": None,
            "name": None,
            "method": "GET",
            "posible_status_code": [200, 404],
            "expected_status_code": 200,
            "expected_text": "health",  # None = any
            "expected_headers": None,
        },  # Done
        {
            "location": "/apikey",
            "name": "baby_yaml",
            "headers": None,
            "params": test_server_params,  # dict(str:str,)
            # {'apikey':"4420d1918bbcf7686defdf9560b"},
            "data": None,
            "method": "GET",
            "posible_status_code": [200, 404, 401],
            "expected_status_code": 200,
            "expected_text": "health",  # None = any
            "expected_headers": None,
        },  # Done
    ],
}

########################### TEST NGINX ##############################
test_server_url_table2 = {
    "name": "WSession-2",# None = any
    "port": ":444",
    "protocol": "https",  # http or https
                         # httpv2 -> https
    
    "ip": proxies_ip,
    "proxies": {
        "http": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
        "https": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
    },
    "verify": False,
    "list_req": [
        {#1
            "location": "/",
            "expected_status_code": 200,# None = any
        },  # 
        {#2
            "location": "/health",
            "name": 'health_httpv2',
            "expected_status_code": 200,# None = any
            "expected_text": "health",  # None = any
            "delay":2.1 , # delay after request
        },  # 
        {#3
            "location": "/apikey",
            "name": "apikey_httpv2",
            "params": test_server_params,
            "posible_status_code": [200,401, 404],# None = any
            "expected_status_code": 200,# None = any
            "expected_text": "health",  # None = any
        },  
        {#4
            "location": "/redirect",
            "name": "httpv2_redirect",
            "method": "GET",# None = GET
            "expected_status_code": 301,# None = any
        },  # 
        {#5
            "location": "/addheader",
            "name": "httpv2_addheader",
            "method": "GET",# None = GET
            "expected_status_code": 200,# None = any
            "expected_headers": 
                {
                    'my_header': "value"
                },
        },  # 

        ],
}
test_server_url_table3 = {
    "name": "WSession-3",# None = any
    "port": ":443",
    "protocol": "https",  # http or https
                         # httpv2 -> https
    
    "ip": proxies_ip,
    "allow_redirects": True,
    "verify": False,
    "list_req": [
        {#1
            "location": "/phealth",
            "name": 'post_1',
            "method": "POST",# None = GET
            "expected_status_code": 200,# None = any
        },  
        {#2
            "location": "/predirect1",
            "name": "post_redirect",
            "method": "POST",# None = GET
            "expected_status_code": 200,# None = any
        },  # Done
        {#3
            "location": "/papikey",
            "params": test_server_params,
            "method": "POST",# None = GET
            "expected_status_code": 200,# None = any
        },  # Done

        ],
}
 
#####################################################################
