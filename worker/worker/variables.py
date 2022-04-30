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
    "port": ":80",
    "protocol": "http",  # http or https
    # httpv2 -> https
    "proxies": {
        "http": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
        "https": f"{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}",
    },
    "timeout": (1, 5),
    "verify": False,
    "locations": [
        {
            "location": "/",
            "name": None,
            "headers": None,
            "params": None,
            "data": None,
            "method": "GET",
            "posible_status_code": [200, 404],
            "expected_status_code": 200,
            "expected_text": "health",  # None = any
            "expected_headers": None,
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
