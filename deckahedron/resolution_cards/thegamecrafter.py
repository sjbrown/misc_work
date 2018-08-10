#! /usr/bin/env python

import os
import requests

base_url="https://www.thegamecrafter.com/api"

session = None
user = None
game = None

class User(dict):
    def __init__(self, udict):
        super(User, self).__init__(udict)
        self.id = udict['id']
        self.designer_id = user_designers(self.id)[0]['id']
        self.games = user_games(self.id)

class Game(dict):
    def __init__(self, gdict, name):
        super(Game, self).__init__(gdict)
        self.id = gdict['id']
        self.folder = new_folder(name)

    def make_square_deck(self, filepath):
        asset = self['name'] + 'sqdk'

        self.sqdk_folder = new_folder(asset, self.folder['id'])
        file_result = new_file(filepath, self.sqdk_folder['id'])
        new_square_deck(asset, self.id, back_id=file_result['id'])

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
    response = requests.get(url, params=params)
    if not str(response.status_code).startswith('2'):
        print 'FAIL', response
        raise Exception('Request failed')
    return response.json()['result']


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

    result = get('/user/' + session['user_id'])
    print 'USER result', result
    user = User(result)

def user_games(user_id):
    result = get('user/%s/games' % user_id)
    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    return result['items']

def user_designers(user_id):
    result = get('user/%s/designers' % user_id)

    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    if len(result['items']) != 1:
        raise NotImplemented('Cannot handle 0 or >1 designers yet')

    return result['items']

def new_game(name):
    global game
    res = post('game',
        name=name,
        designer_id=user.designer_id,
        description='Automatically created (%s)' % name,
    )
    game = Game(res, name)

def new_square_deck(name, game_id, back_id=None):
    res = post('smallsquaredeck',
        name=name,
        game_id=game_id,
        back_id=back_id,
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
    if not os.path.isfile(filepath):
        raise Exception('Not a file: %s' % filepath)
    fp = file(filepath)
    filename = os.path.basename(filepath)
    res = post('file', files={'file':fp}, name=filename, folder_id=folder_id)
    return res

