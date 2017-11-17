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
    if 'circles' not in d2:
        d2['circles'] = []
    elif d2['circles'] == '':
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
        print 'levels', d2[k]
        if d2[k] != '':
            if '*' in d2[k]:
                d2['level_start'] = v
            if d2['attr']:# 'spot' not in d2[k].lower():
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
    i = 0
    for k,new_key in spot_map.items():
        new_val = d2[k].strip()
        if re.search('\d', new_val) and re.search('\d', new_val).group() != '1':
            raise Exception('not able to handle numbers, but it would be easy')
        if 'SPOT' in new_val.upper() and 'EX' in new_val:
            d2['spots'][i] = ['EX']
        elif 'SPOT' in new_val.upper() and 'BR' in new_val:
            d2['spots'][i] = ['BR']
        i += 1

def parse_tags(d2):
    tags = d2.get('tags')
    if not tags:
        d2['tags'] = []
    else:
        d2['tags'] = tags.split(',')

def parse_reqs(d2):
    d2['reqs'] = d2.get('reqs')

def parse_flags(d2):
    possible_flags = [
      'IMMEDIATE',
      'ONGOING',
      'UNENCUMBERED',
      'RECEIVE CARDS',
    ]
    d2['flags'] = []
    note = d2.get('flags') or d2.get('note') or d2.get('notes') or ''
    if not note.strip():
        return
    flags = [x.strip() for x in note.split(',')]
    if any(x not in possible_flags for x in flags):
        raise Exception('How to flags ?? %s' % flags)
    print 'set', set(flags)
    d2['flags'] = flags

def parse_desc(d2):
    desc_detail = ''
    body = d2.get('desc') or d2.get('effect')
    bulleted = body.split('*')
    preamble = bulleted.pop(0).strip()
    if bulleted:
        bulleted = ['\n' + u'✷' + x.strip() for x in bulleted]
    desc_detail = preamble + ''.join(bulleted)

    desc_detail = parse_text(desc_detail)
    d2['desc_detail'] = desc_detail


def parse_text(text):
    if not text:
        return text
    text = text.strip()
    parts = text.split('|')
    text = '\n'.join([x.strip() for x in parts])
    return text

def parse_checks(d2):
    two_x = parse_text(d2.get('r-2') or d2.get('✗✗'))
    one_x = parse_text(d2.get('r-1') or d2.get('✗'))
    one_check = parse_text(d2.get('r1') or d2.get('✔'))
    two_check = parse_text(d2.get('r2') or d2.get('✔✔'))
    if one_check == one_x:
        d2['x_check'] = one_check
    else:
        d2['one_check'] = one_check
        d2['one_x'] = one_x
    d2['two_x'] = two_x
    d2['two_check'] = two_check

def parse_attr(d2):
    d2['attr'] = d2['mod'].strip()

def parse_title(d2, title):
    d2['title'] = title.decode('utf-8').strip().replace('_', '____')

def get_dicts_from_spreadsheet(fname, extra_fields=None, grep_filter=''):
    if extra_fields is None:
        extra_fields = {}

    f = UTF8File(fname)
    spreadsheet = csv.DictReader(f)

    l = []
    for row in spreadsheet:
        name = row.get('name') or row.get('deckahedron move')
        if not name:
            continue
        if grep_filter and grep_filter not in name.lower():
            print 'filtering out', name
            continue
        print 'Processing', name
        d2 = extra_fields.copy()
        d2.update( {k:v.decode('utf-8') for (k,v) in row.items()} )
        parse_title(d2, name)
        parse_circles(d2)
        parse_attr(d2)
        parse_levels(d2)
        parse_desc(d2)
        parse_checks(d2)
        parse_spots(d2)
        parse_tags(d2)
        parse_flags(d2)
        parse_reqs(d2)

        l.append(d2)

    f.close()

    return l

def get_dicts(grep_filter=''):
    return (
      get_dicts_from_spreadsheet(
          'character_move_sheet.csv',
          grep_filter=grep_filter
      )
      +
      get_dicts_from_spreadsheet(
          'equipment_sheet.csv',
          {'equipment': True},
          grep_filter=grep_filter
      )
    )

class DictObj(dict):
    __name__ = 'DICTOBJ'
    def __getattr__(self, attrname):
        if attrname in self:
            return self[attrname]
        raise AttributeError(attrname)

def get_objs(grep_filter=''):
    return [DictObj(x) for x in get_dicts(grep_filter)]
