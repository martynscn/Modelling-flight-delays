#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from getpass import getpass
from pprint import pprint
import requests, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AUTH_URL = "https://zen-cpd-zen.apps.cpd2.power.10.3.75.50.nip.io/icp4d-api/v1/authorize"

MODEL_URL = "https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/d6cf2505-defc-4756-9b03-203f7a22ee33/predictions?version=2021-07-22" # TODO place your model URL here <==================================


# 1. Get authentication token

headers = {
    "Content-Type": "application/json", 
    "cache-control": "no-cache"
}
# payload = {"username": input("Username: "), "password": getpass("Password: ")}
rsp = requests.post(AUTH_URL, json=payload, headers=headers, verify=False)
if rsp.status_code != 200:
    raise Exception("Token request failed: %s" % rsp.text)
token = rsp.json()["token"]


# 2. Create data to predict

data = { # TODO modify data to predict here <=====================================
    "DAY_OF_MONTH": 3,
    "DAY_OF_WEEK": 4,
    "DEP_TIME_BLK": "1700-1759",
    "DEST": "DTW",
    "DISTANCE": 383.0,
    "OP_UNIQUE_CARRIER": "YV",
    "ORIGIN": "IAD",
    "TAIL_NUM": 506
}

fields, values = zip(*data.items())


# 3. Run prediction

headers = {
    "Content-Type": "application/json", 
    "Authorization": "Bearer " + token
}

payload = {"input_data": [{"fields": fields, "values": [[str(x) for x in values]]}]}
rsp = requests.post(MODEL_URL, json=payload, headers=headers, verify=False)
if rsp.status_code != 200:
    raise Exception("Model request failed: %s" % rsp.text)
output = rsp.json()["predictions"][0]["values"][0]


# 4. Display prediction

print("##### Input #####")
pprint(data)
print()
print("##### Output #####")
print("Predicted flight status:", output[0])
print("\n")


