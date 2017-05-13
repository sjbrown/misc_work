import csv


class UTF8File(object):
    def __init__(self, fpath):
        self._data = file(fpath)

    def next(self):
        s = self._data.next()
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
            d2['levels'].append(v)

def parse_desc(d2):
    body = d2['desc']
    note = d2['note'].strip()
    bulleted = body.split('*')
    preamble = bulleted.pop(0).strip()
    if bulleted:
        bulleted = ['\n* ' + x.strip() for x in bulleted]
    d2['desc'] = preamble + ''.join(bulleted)
    if note:
        d2['desc'] += '\n| ' + note

def parse_checks(d2):
    two_x = d2['r-2'].strip()
    one_x = d2['r-1'].strip()
    one_check = d2['r1'].strip()
    two_check = d2['r2'].strip()
    if one_check == one_x:
        d2['x_check'] = one_check
    else:
        d2['one_check'] = one_check
        d2['one_x'] = one_x
    d2['two_x'] = two_x
    d2['two_check'] = two_check

def get_dicts():
    f = UTF8File('character_move_sheet.csv')
    r = csv.DictReader(f)

    l = []
    for d1 in r:
        if not d1['name']:
            continue
        d2 = {k:v.decode('utf-8') for (k,v) in d1.items()}
        d2['title'] = d2['name']
        parse_circles(d2)
        parse_levels(d2)
        parse_desc(d2)
        parse_checks(d2)

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
