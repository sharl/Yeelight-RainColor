import math
import datetime as dt

import requests


def deg2dec(deg):
    degree, minute = deg
    return degree + minute / 60


def getNearAmedas(lat, lng):
    with requests.get('https://www.jma.go.jp/bosai/amedas/const/amedastable.json') as r:
        lines = []
        data = r.json()
        for key in data:
            name = data[key]['kjName']
            elem = data[key]['elems']
            _lat = deg2dec(data[key]['lat'])
            _lng = deg2dec(data[key]['lon'])
            dist = math.dist((lat, lng), (_lat, _lng))
            # snow
            if elem[5] == '1':
                lines.append([key, name, dist])

        return sorted(lines, key=lambda x: x[2])[0]

    return []


def isSnowy(lat, lng):
    code, name, _ = getNearAmedas(lat, lng)

    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))) - dt.timedelta(minutes=10)
    yyyymmdd = now.strftime('%Y%m%d')
    HH = now.strftime('%H')
    hh = f'{int(HH) // 3 * 3:02d}'
    url = f'https://www.jma.go.jp/bosai/amedas/data/point/{code}/{yyyymmdd}_{hh}.json'
    with requests.get(url, timeout=10) as r:
        data = r.json()
        base_key = f'{yyyymmdd}{HH}0000'        # 積雪は1時間毎    pass
        cm, valid = data[base_key].get('snow', [None, None])
        if valid is not None and cm is not None:
            return True

    return False
