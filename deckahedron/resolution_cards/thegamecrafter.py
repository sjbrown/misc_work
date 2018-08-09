#! /usr/bin/env python

import os
import requests

#private_key = os.environ.get('THEGAMECRAFTER_PRIVATE_KEY')

base_url="https://www.thegamecrafter.com/api"

session = None
user = None

def login():
    params = {
        'api_key_id': os.environ.get('THEGAMECRAFTER_PUBLIC_KEY'),
        'username' : os.environ.get('THEGAMECRAFTER_USER'),
        'password': os.environ.get('THEGAMECRAFTER_PASSWORD'),
    }
    response = requests.post(base_url + "/session", params=params)
    print 'LOGIN RESPONSE', response.json()
    if response.status_code == 200:
        session = response.json()['result']
    else:
        raise Exception('Could not log in. Check your environment variables')

    response = requests.get(
        base_url + '/user/' + session['user_id'],
        params = {'session_id': session['id']}
    )
    print 'USER RESPONSE', response.json()
    if response.status_code == 200:
        user = response.json()['result']
    else:
        raise Exception('Could not get user info.')

def post(endpoint, files=None, **kwargs):
    if session is None:
        raise Exception('Must be logged in before post() can be called')

    url = base_url
    if not endpoint.startswith('/'):
        url += '/'
    url += endpoint

    params['session_id'] = session['id']
    print 'POST', url, params.keys()
    return requests.post(url, params=params, files=files)


login()
