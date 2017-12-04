import requests,json,os
import win32gui,win32api,win32con
urlbase='https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&pid=hp'
r=requests.get(urlbase)
r=r.json()
url='https://cn.bing.com'+r[u'images'][0][u'urlbase']+'_1920x1080.jpg'
pic=requests.get(url)
with open(r'C:\Users\chun\Pictures\1.jpg','wb')as f:
    f.write(pic.content)
    f.close()
k=win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")
win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,r'C:\Users\chun\Pictures\1.jpg',1+2)
