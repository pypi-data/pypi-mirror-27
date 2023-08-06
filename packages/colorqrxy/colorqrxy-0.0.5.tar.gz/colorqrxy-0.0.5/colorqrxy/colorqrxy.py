from MyQR import myqr
from PIL import Image
import urllib.request as req
from random import randint
import time


def _get_width(picture):
    im = Image.open(picture,'r')
    version = int(im.size[0]/100)
    if version >=10:
        version = 10
    elif version <= 1:
        version = 1
    im.close()
    return version
'''
生成普通验证码
data:写入的数据
save_name:生成二维码保存的名字
'''
def create_qr(data,save_name='qrcode.png'):
	myqr.run(data,save_name=save_name)

'''
通过url图片产生二维码
'''
def create_url_qr(data,url,colorized=True):
    url = url.replace('https','http')
    picture = str(int(time.time()))+'_'+str(randint(1000,9999)) + url[-4:]
    req.urlretrieve(url,picture)
    version = _get_width(picture)
    save_name = picture + '.png'
    myqr.run(data,picture=picture,save_name=save_name,version=version,colorized=colorized)

'''
生成带背景图片的二维码
picture:背景图片的路径及名称
'''
def create_pic_qr(data,picture,save_name='qrcode.png'):
    version = _get_width(picture)
    myqr.run(data,picture=picture,save_name=save_name,version=version)

'''
生成彩色图片验证码
'''
def create_color_qr(data,picture,save_name='qrcode.png'):
    version = _get_width(picture)
    myqr.run(data,picture=picture,save_name=save_name,colorized=True,version=version)

'''
生成gif动态验证码
'''
def create_gif_qr(data,picture,save_name='qrcode.gif'):
    version = _get_width(picture)
    myqr.run(data,picture=picture,save_name=save_name,colorized=True,version=version)
