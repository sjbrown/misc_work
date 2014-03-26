#! /usr/bin/env python

from django.http import HttpResponse
from django.utils import simplejson as json

class JsonResponse(HttpResponse):
    def __init__(self, content, *args, **kwargs):
        kwargs['content_type'] = 'application/json'
        kwargs['mimetype'] = 'application/json'
        kwargs['content'] = json.dumps(content)
        super(JsonResponse, self).__init__(*args, **kwargs)

def hello(request, **kwargs):
    return JsonResponse("HELLO WORLD")

def echo(request, **kwargs):
    url = request.GET['url']

    return JsonResponse(dict(request.GET))


product_birch_set = dict(
url='http://www.amazon.com/Hand-Made-Wooden-Board-Birch/dp/B00IVTWPV4',
title='Boardcrafting Birch Set - Wooden Settlers of Catan Board',
price='386.00',
currency_code='USD',
provider_name='Amazon',
description='''\
The Boardcrafting Birch Set is an artisan-crafted accessory
for Settlers of Catan.
It includes a leather-backed frame, tiles, pips, ports, and
a robber, and turns your game table into something really special.
The pieces in this set are made of baltic birch, finished with lacquer.
The leather backing allows the frame to fold.
After the wood is laser-cut and etched, I hand-sand it where needed
and then a clear coat is applied to protect the wood and give it a
beautiful gloss. I designed the tiles to have the same dimensions as
the tiles from the Mayfair Games 4th edition (red box) version of Catan.
You will need a copy of the official game to play with this board
(for the cards, cities, roads, etc).
''',
brand='Boardcrafting',
product_id='BIRCH0001',
availability='in stock',
quantity=3,
standard_price='430.00',
geographic_availability='All',
images = [
          'http://ezide.com/showcase/board_main.jpg',
          'http://ezide.com/showcase/catan_showcase_118.jpg',
          'http://ezide.com/showcase/tiles02.jpg',
         ],
referenced_items = [
 'http://www.amazon.com/MayFair-Games-MFG3061-Settlers-Catan/dp/B000W7JWUA/',
 'https://en.wikipedia.org/wiki/The_Settlers_of_Catan',
 'http://www.catan.com/',
],
rating='5.0',
rating_scale='5.0',
rating_count='1',
)

def query(request, **kwargs):
    url = request.GET['url']

    return JsonResponse(product_birch_set)

