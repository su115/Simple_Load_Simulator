import requests
import pytest
import os
import ast
from worker.tests.json.data import *

# this test file will test worker by data{1..4}.json
# and will check by hard locked vales
@pytest.mark.network
def test_API_by_data_json():
    path = os.path.dirname( os.path.realpath(__file__) )
    headers = {'Content-Type' : 'application/json'}
    url = "http://localhost:7799/worker"
    for key in hard_data:
        #with open(path +)
        answer = requests.post(url, data=open(path + key, 'rb'), headers=headers)
        print('-'*18)
        print(path+key)
        print("answer:   ",answer.text)
        print("harddata: ",hard_data[key])
        print('-'*18)
        
        assert hard_data[key] in answer.text

@pytest.mark.network
def test_API_by_data_json_network():
    path = os.path.dirname( os.path.realpath(__file__) )
    headers = {'Content-Type' : 'application/json'}
    url = "http://localhost:7799/worker"
    for key in hard_data_network:
        answer = requests.post(url, data=open(path + key, 'rb'), headers=headers)
        print(path+key)
        assert answer.text.count(hard_data_network[key][0]) == hard_data_network[key][1]
