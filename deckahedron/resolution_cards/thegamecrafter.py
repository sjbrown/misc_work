#! /usr/bin/env python

import os
import requests

public_key = os.environ('GAMECRAFTER_PUBLIC_KEY')
private_key = os.environ('GAMECRAFTER_PRIVATE_KEY')


url="https://www.thegamecrafter.com/api"

params = {'api_key_id': api_key_id, 'username' : username, 'password': password}
response = requests.post(url + "/session", params=params)
if response.status_code==200:
    print("----Status code OK!----")
    print("---Get a session---")
    print(response.json())
    print("-------------------")
    session = response.json()['result']

