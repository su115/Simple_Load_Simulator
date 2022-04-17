from worker.variables import *
import yaml, os

# Static yaml
def get_yaml_file():
    data = {
            'name': "test1",
            "proxies": {
                 'http':  f'{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}',
                 'https': f'{proxies_protocol}://{proxies_user}:{proxies_pass}@{proxies_ip}:{proxies_port}',
                 },
            "list_req": [
                    {
                        "name": "Test 1",
                        "method": "GET",
                        "url": test_server_url,
                        "headers": {
                            "id": "1",
                            "test": "yes",
                            },
                        "params": {
                            "more": "yes",
                            },
                        "data": {
                            "some": "data",
                            },
                    },
                    {
                        "name": "Test 2",
                        "method": "GET",
                        "url": test_server_url,
                        "headers": {
                            "id": "1",
                            "test": "yes",
                            },
                        "data": {
                            "some": "data",
                            },
                    },

                    {
                        "name": "Test 3",
                        "method": "GET",
                        "url": test_server_url,
                        "headers": {
                            "id": "1",
                            "test": "yes",
                            },
                        "params": {
                            "more": "yes",
                            },
                    },
                    {
                        "name": "Test 4",
                        "method": "GET",
                        "url": test_server_url,
                        "params": {
                            "more": "yes",
                            },
                        "data": {
                            "some": "data",
                            },
                    },
                    {
                        "name": "Test 5",
                        "method": "GET",
                        "url": test_server_url,
                    },
                ],
            }
    path = os.path.dirname(os.path.realpath(__file__))
    with open( path + '/WRequest_1.yaml','w' ) as f:
        yaml.dump(data,f,default_flow_style=False)
