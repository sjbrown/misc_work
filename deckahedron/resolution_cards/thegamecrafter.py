#! /usr/bin/env python

import os
import requests

#private_key = os.environ.get('THEGAMECRAFTER_PRIVATE_KEY')

base_url="https://www.thegamecrafter.com/api"

session = None
user = None
game = None

class User(dict):
    pass

class Game(dict):
    pass

def login():
    global session, user
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

    response = get('/user/' + session['user_id'])
    print 'USER RESPONSE', response.json()
    if response.status_code == 200:
        user = User(response.json()['result'])
        user.id = user['id']
        user_designers()
        user_games()
    else:
        raise Exception('Could not get user info.')

def post(endpoint, files=None, **kwargs):
    if session is None:
        raise Exception('Must be logged in before post() can be called')

    url = base_url
    if not endpoint.startswith('/'):
        url += '/'
    url += endpoint

    params = kwargs
    params['session_id'] = session['id']
    print 'POST', url, params.keys()
    response = requests.post(url, params=params, files=files)

    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        raise Exception('Request failed')

    return response.json()['result']

def get(endpoint, **kwargs):
    if session is None:
        raise Exception('Must be logged in before get() can be called')

    url = base_url
    if not endpoint.startswith('/'):
        url += '/'
    url += endpoint

    params = kwargs
    params['session_id'] = session['id']
    print 'GET', url, params.keys()
    return requests.get(url, params=params)

def user_games():
    result = get('user/%s/games' % user['id']).json()['result']
    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    user.games = result['items']
    return result['items']

def user_designers():
    result = get('user/%s/designers' % user['id']).json()['result']

    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')

    user.designers = result['items']

    if len(user.designers) != 1:
        raise NotImplemented('Cannot handle 0 or >1 designers yet')

    user.designer_id = result['items'][0]['id']
    return result['items']

def new_game(name):
    global game
    res = post('game',
        name=name,
        designer_id=user.designer_id,
        description='Automatically created (%s)' % name,
    )
    game = Game(res)
    game.id = game['id']
    game.folder = new_folder(name)

def new_square_deck(name):
    res = post('smallsquaredeck',
        name=name,
        game_id=game.id
    )
    return res

def new_folder(asset_name, parent_id=None):
    if parent_id is None:
        parent_id = user['root_folder_id']
    res = post('folder',
        name=asset_name,
        user_id=user.id,
        parent_id=parent_id,
    )
    return res

def new_file(filepath, folder_id):
    fp = file(filepath)
    filename = os.path.basename(filepath)
    res = post('file', files={'file':fp}, name=filename, folder_id=folder_id)
    return res

