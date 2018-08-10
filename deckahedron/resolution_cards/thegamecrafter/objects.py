#! /usr/bin/env python

import os
from . import core

user = None
game = None

class User(dict):
    def __init__(self):
        udict = core.login()
        super(User, self).__init__(udict)
        self.id = udict['id']
        self.designer_id = user_designers(self.id)[0]['id']
        self.games = user_games(self.id)

class Game(dict):
    def __init__(self, name):
        gdict = core.new_game(name)
        super(Game, self).__init__(gdict)
        self.id = gdict['id']
        self.folder = new_folder(name)

    def make_square_deck(self, filepath):
        asset = self['name'] + 'sqdk'

        self.sqdk_folder = new_folder(asset, self.folder['id'])
        file_result = new_file(filepath, self.sqdk_folder['id'])
        new_square_deck(asset, self.id, back_file_id=file_result['id'])


def user_games(user_id):
    result = core.get('user/%s/games' % user_id)
    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    return result['items']

def user_designers(user_id):
    result = core.get('user/%s/designers' % user_id)

    if result['paging']['total_pages'] > 1:
        raise NotImplemented('Cannot handle pages yet')
    if len(result['items']) != 1:
        raise NotImplemented('Cannot handle 0 or >1 designers yet')

    return result['items']

def new_square_deck(name, game_id, back_file_id=None):
    res = core.post('smallsquaredeck',
        name=name,
        game_id=game_id,
        back_file_id=back_file_id,
    )
    return res

