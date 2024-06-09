# -*- coding: utf-8 -*-
import os
import time
import io
import threading
import tomllib
import webbrowser

import schedule
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import requests
from bs4 import BeautifulSoup
from yeelight import Bulb

NAME = 'Yeelight Rain Color'

INTERVAL = 5 * 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class taskTray:
    def __init__(self):
        self.running = False
        self.base = []

        self.readConf()

        item = []
        item.append(MenuItem('Open', self.doOpen, default=True, visible=False))
        item.append(MenuItem('Check', self.doTask))
        item.append(MenuItem('Reload', self.readConf))
        item.append(MenuItem('Exit', self.stopApp))
        menu = Menu(*item)

        # 初期アイコン
        self.image = Image.new('RGB', (32, 32), WHITE)
        self.draw = ImageDraw.Draw(self.image)
        self.app = Icon(name=NAME, title=NAME, icon=self.image, menu=menu)

        self.doTask()

    def readConf(self):
        home = os.environ.get('HOME', '.')
        with open(f'{home}/.yeelight-raincolor', 'rb') as fd:
            data = tomllib.load(fd)
            self.base = data.get('location', '').strip().split('?')
            self.bulb = Bulb(data.get('bulb'))
            self.rgb = data.get('rgb')

    def doTask(self):
        r, g, b = self.getRGB()
        rgb = f'{r} {g} {b}'
        print(rgb, self.rgb)

        if rgb == self.rgb:
            self.bulb.turn_off()
            self.draw.rectangle((0, 0, 31, 31), fill=BLACK, outline=WHITE)
        else:
            self.draw.rectangle((0, 0, 31, 31), fill=(r, g, b), outline=WHITE)
            self.bulb.turn_on()
            self.bulb.set_rgb(r, g, b)

        self.app.title = f'{NAME} - {rgb}'
        self.app.icon = self.image
        self.app.update_menu()

    def doOpen(self):
        url = '?'.join(self.base)
        webbrowser.open(url)

    def stopApp(self):
        self.running = False
        self.app.stop()

    def runSchedule(self):
        schedule.every(INTERVAL).seconds.do(self.doTask)

        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def runApp(self):
        self.running = True

        task_thread = threading.Thread(target=self.runSchedule)
        task_thread.start()

        self.app.run()

    def getRGB(self):
        base_url = f'{self.base[0]}?{self.base[1]}'
        r = requests.get(base_url)
        if r and r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            og_images = soup.find_all('meta', property='og:image')
            if len(og_images) == 0:
                return BLACK
            img_url = og_images[0].get('content').replace('1200x630', '1x1')

            r = requests.get(img_url)
            if r and r.status_code == 200:
                image = Image.open(io.BytesIO(r.content)).convert('RGB')
                return image.getpixel((0, 0))

        return BLACK


if __name__ == '__main__':
    taskTray().runApp()
