#! /usr/bin/env python

from django.http import HttpResponse

def home(request, **kwargs):
    return HttpResponse("HELLO WORLD")


