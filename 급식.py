import requests
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap3
import ctypes, win32con, os
import datetime

def setWallpaper(path):
    changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER,0,path,changed)

def make_image(date, message1, message2, message3):
    W = 1920
    H = 1080
    bg_color = 'rgb(255, 255, 255)'
    
    # font setting
    font = ImageFont.truetype('malgun.ttf', size=55)
    font_color = 'rgb(0, 0, 0)' 
    
    image =Image.new('RGB', (W, H), color = bg_color)
    draw = ImageDraw.Draw(image)
    
    lines = [date, '<아침>']
    lines = lines + textwrap3.wrap(message1, width=30) + ['<점심>'] + textwrap3.wrap(message2, width=30) + ['<저녁>'] + textwrap3.wrap(message3, width=30)
  
    x_text = 50
    y_text = 150
    
    for line in lines:
        width, height = font.getsize(line)
        draw.text(((W-width)/2, y_text), line, font=font, fill=font_color)
        y_text += height
    image.save('급식.png')


meal_order = 1 #0~2
today = datetime.datetime.now()
date = today.strftime('%Y%m%d')
if(int(today.hour) >= 18) : 
    date = date[0:6]+str(int(date[6:8])+1).zfill(2)

url = 'https://open.neis.go.kr/hub/mealServiceDietInfo?Type=json&KEY=7c8f58d4e4174b94b96b1aea5fb6fd0d&ATPT_OFCDC_SC_CODE=I10&SD_SCHUL_CODE=9300054&MLSV_YMD='+date
response = requests.get(url)
school_menu = json.loads(response.text)
dish = ['', '', '']
dish[0]=dish[1]=dish[2]='어머, 급식이 없네요'
print(len(school_menu['mealServiceDietInfo'][1]['row']))
for i in range(len(school_menu['mealServiceDietInfo'][1]['row'])) :
    dish[i] = school_menu['mealServiceDietInfo'][1]['row'][i]['DDISH_NM']


characters = ".0987654321"
for x in range(len(characters)):
    dish[0] = dish[0].replace(characters[x],"")
    dish[1] = dish[1].replace(characters[x],"")
    dish[2] = dish[2].replace(characters[x],"")

dish[0] = dish[0].replace('<br/>'," ")
dish[1] = dish[1].replace('<br/>'," ")
dish[2] = dish[2].replace('<br/>'," ")


make_image(date, dish[0], dish[1], dish[2])
path = os.path.abspath('급식.png')
setWallpaper(path)