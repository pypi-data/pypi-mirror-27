from MyQR import myqr


'''
生成普通验证码
data:写入的数据
save_name:生成二维码保存的名字
'''
def create_qr(data,save_name='qrcode.png'):
	myqr.run(data,save_name=save_name)

'''
生成带背景图片的二维码
picture:背景图片的路径及名称
'''
def create_pic_qr(data,picture,save_name='qrcode.png'):
    myqr.run(data,picture=picture,save_name=save_name)

'''
生成彩色图片验证码
'''
def create_color_qr(data,picture,save_name='qrcode.png'):
    myqr.run(data,picture=picture,save_name=save_name,colorized=True)

'''
生成gif动态验证码
'''
def create_gif_qr(data,picture,save_name='qrcode.gif'):
    myqr.run(data,picture=picture,save_name=save_name,colorized=True)
