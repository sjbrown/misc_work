#! /usr/bin/env python

import os
import core

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
    def __init__(self, user, name):
        self.user = user
        gdict = core.new_game(user, name)
        super(Game, self).__init__(gdict)
        self.id = gdict['id']
        self.folder = core.new_folder(user, name)

    def make_square_deck(self, dirpath):
        asset = self['name'] + 'sqdk'

        back_filepath = dirpath + '/back.png'

        self.sqdk_folder = core.new_folder(self.user, asset, self.folder['id'])
        file_result = core.new_file(back_filepath, self.sqdk_folder['id'])
        sqdk = new_square_deck(asset, self.id, back_file_id=file_result['id'])

        print 'Small Square Deck'
        print sqdk

        file_list = os.listdir(dirpath)
        file_list = [dirpath + '/' + x for x in file_list
                     if (x.startswith('deck') and x.endswith('.png'))]
        for filepath in file_list:
            file_result = core.new_file(filepath, self.sqdk_folder['id'])
            card = new_card(
                'smallsquarecard',
                os.path.basename(filepath),
                deck_id=sqdk['id'],
                file_id=file_result['id']
            )


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
        back_id=back_file_id,
    )
    return res

def new_card(kind, name, deck_id, file_id=None):
    res = core.post(
        kind,
        name=name,
        deck_id=deck_id,
        face_id=file_id,
        has_proofed_face=True,
    )
    return res

