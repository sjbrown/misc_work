#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv



class UTF8File(object):
    def __init__(self, fpath):
        self._data = file(fpath)
        self._firstLine = True

    def next(self):
        s = self._data.next()
        if self._firstLine:
            s = s.lower()
            self._firstLine = False
        #print 'data line', s
        # Google Sheets puts those annoying UTF-8 apostrophes and dashes in the file
        s = s.replace('\xe2\x80\x93', '-')
        s = s.replace('\xe2\x80\x99', "'")
        return s

    def close(self):
        self._data.close()

    def __iter__(self):
        return self

def parse_circles(d2):
    if d2['circles'] == '':
        d2['circles'] = []
    else:
        d2['circles'] = [x.strip() for x in d2['circles'].split(',')]

def parse_levels(d2):
    d2['levels'] = []
    level_map = {
        'm-2': 'r2',
        'm-1': 'r1',
        'm0': '0',
        'm1': 'g1',
        'm2': 'g2',
    }
    for k,v in level_map.items():
        if d2[k] != '':
            if '*' in d2[k]:
                d2['level_start'] = v
            d2['levels'].append(v)

def parse_spots(d2):
    spot_map = {
        'm-2': -2,
        'm-1': -1,
        'm0': 0,
        'm1': 1,
        'm2': 2,
    }
    d2['spots'] = {}
    for k,new_key in spot_map.items():
        new_val = d2[k].strip()
        if 'EX' in new_val:
            d2['spots'][new_key] = append('EX')
        elif 'BR' in new_val:
            d2['spots'][new_key] = append('BR')

def parse_desc(d2):
    body = d2.get('desc') or d2.get('effect')
    note = d2.get('note') or d2.get('notes')
    note = note.strip()
    bulleted = body.split('*')
    preamble = bulleted.pop(0).strip()
    if bulleted:
        bulleted = ['\n* ' + x.strip() for x in bulleted]
    d2['desc_detail'] = preamble + ''.join(bulleted)
    if note:
        d2['desc_detail'] += '\n| ' + note

def parse_checks(d2):
    two_x = (d2.get('r-2') or d2.get('✗✗')).strip()
    one_x = (d2.get('r-1') or d2.get('✗')).strip()
    one_check = (d2.get('r1') or d2.get('✔')).strip()
    two_check = (d2.get('r2') or d2.get('✔✔')).strip()
    if one_check == one_x:
        d2['x_check'] = one_check
    else:
        d2['one_check'] = one_check
        d2['one_x'] = one_x
    d2['two_x'] = two_x
    d2['two_check'] = two_check

def parse_attr(d2):
    d2['attr'] = d2['mod']

def get_dicts():
    f = UTF8File('character_move_sheet.csv')
    spreadsheet = csv.DictReader(f)

    l = []
    for row in spreadsheet:
        name = row.get('name') or row.get('deckahedron move')
        if not name:
            continue
        d2 = {k:v.decode('utf-8') for (k,v) in row.items()}
        d2['title'] = name.decode('utf-8')
        parse_circles(d2)
        parse_levels(d2)
        parse_desc(d2)
        parse_checks(d2)
        parse_attr(d2)

        l.append(d2)

    f.close()

    return l

class DictObj(dict):
    __name__ = 'DICTOBJ'
    def __getattr__(self, attrname):
        if attrname in self:
            return self[attrname]
        raise AttributeError(attrname)

def get_objs():
    return [DictObj(x) for x in get_dicts()]