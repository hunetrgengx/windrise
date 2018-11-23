#pyinstaller -w vcode1.py
from PIL  import Image
import win32api
import time
import win32con
import random
import win32gui
from PIL import ImageGrab
def get_hash(img):
         #使用PIL模块缩放图片,***
     image = img.resize((18, 13), Image.ANTIALIAS).convert("L")
     pixels = list(image.getdata())
     avg = sum(pixels) / len(pixels)
     return "".join(map(lambda p : "1" if p > avg else "0", pixels))

def hamming(hash1, hash2, n=20):
    b = False
    assert len(hash1) == len(hash2)
    if sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)) < n:
        b = True
    return b

def click(x, y, t=0):  # 移动鼠标并点击左键
    win32api.SetCursorPos((x, y))  # 设置鼠标位置(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)  # 点击鼠标左键
    time.sleep(random.random()*2)

# 查看图片
#左上右下
'''
img = ImageGrab.grab((1,100,100,100))
img.save('addrrrr.jpg','jpeg')
img = Image.open('1.jpg') #打开当前路径图像
box1 = (14, 4, 53, 52)    #设置图像裁剪区域
image1 = img.crop(box1)   #图像裁
image1.save('image1.jpg')  #存储当前区域
im = ImageGrab.grab()
im.save('addr.jpg','jpeg')
img.show()
'''


#存储常用数据：
yes=()  #确定按钮



tuple_aa=(462,320,514,401)
hash_aa=get_hash(Image.open('aa.png'))




aa=get_hash(ImageGrab.grab(tuple_aa))
hamming(aa,hash_aa)
if hamming(aa,hash_aa):
    print(aa)
else:
    print('失败')




def ifclick(name,n=1):
    a=get_hash(Image.open(name[0]+'.png'))      
    b=get_hash(ImageGrab.grab(name[1:]))
    while not hamming(a,b):
        time.sleep(n)
        b=get_hash(ImageGrab.grab(name[1:]))
    click(int((name[1]+name[3])/2),int((name[2]+name[4])/2))
    time.sleep(random.random())

def ifok(name,n=1):
    a=get_hash(Image.open(name[0]+'.png'))      
    b=get_hash(ImageGrab.grab(name[1:]))
    while not hamming(a,b):
        time.sleep(n)
        b=get_hash(ImageGrab.grab(name[1:]))
    c = True
    return c

def tclick(name):
    click(int((name[1]+name[3])/2),int((name[2]+name[4])/2))
    time.sleep(random.random())


def niluji():
    ifclick()

t_enter=('t_enter',641,195,1217,311)
ifclick(t_enter)


t_friend2=('t_friend2',88,421,242,560)
ifclick(t_friend2)

t_start=('t_start',1092,637,1264,724)
ifclick(t_start)


t_kmgj=('t_kmgj',861,557,929,623)
ifclick(t_kmgj)
t_yes=('t_yes',702,412,1005,473)
ifclick(t_yes)

t_kmfy=('t_kmfy',771,556,840,625)
ifclick(t_kmfy)
t_yes=('t_yes',702,412,1005,473)
ifclick(t_yes)
print('a')


t_attack=('t_attack',1046,581,1217,657)
ifclick(t_attack)
#da zhao wu fa du qu 
t_atbig2=('t_atbig2',577,127,739,341)
ifclick(t_atbig2)



t_at1=('t_at1',87,382,252,619)
t_at2=('t_at2',332,377,500,635)


t_atspeed1=('t_atspeed1',763,69,1211,151)
while ifok(t_atspeed1):
    time.sleep(random.random()+0.5)
    tclick(t_atbig2)
    tclick(t_at1)
    time.sleep(random.random())
    tclick(t_at2)
    time.sleep(random.random())
    time.sleep(random.random())
    break

