# Yeelight-RainColor

Yahoo 雨雲レーダー画像を取得して降水量の色を Yeelight の RGB ランプに反映

## Run

```
git clone https://github.com/sharl/Yeelight-RainColor.git
cd Yeelight-RainColor
pip install -r requirements.txt
python Yeelight-RainColor.py
```

## .yeelight-raincolor

```
location = "https://weather.yahoo.co.jp/weather/zoomradar/?lat=42.923&lon=143.193&z=12"
bulb = "192.168.0.204 192.168.0.220"
# broadcast = "192.168.0.255"
rgb = "252 252 248"
```

### location

緯度・経度・拡大率が含まれている [雨雲レーダー](https://weather.yahoo.co.jp/weather/zoomradar/) の URL

### bulb

Yeelight RGB デバイスの IP アドレス 空白区切りで複数指定可能

### broadcast

対象ネットワークのすべての Yeelight RGB デバイスを使用

### rgb

雨が降っていないときの観測地点の色

この色と異なる場合に RGB デバイスが点灯
