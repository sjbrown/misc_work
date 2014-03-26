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

def query(request, **kwargs):
    return JsonResponse({'greeting':"HELLO WORLD"})

