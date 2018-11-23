http://www.msweet.com.cn/eportal/ui?pageId=1013961&currentPage='+str(i)+'&moduleId=e2569b5046d44d22abfa530608628071&staticRequest=yes

import requests,re
from bs4 import BeautifulSoup
target ='http://www.msweet.com.cn/eportal/ui?pageId=1013961&currentPage='+str(i)+'&moduleId=e2569b5046d44d22abfa530608628071&staticRequest=yes'
req = requests.get(url=target)#requests获取请求
req.encoding = 'utf-8'        #定义encoding
html = req.text               #取req的属性
bf = BeautifulSoup(html,'lxml')
texts = bf.find_all('div', class_ = 'list-recommend normal-recommend')

bd=BeautifulSoup(str(texts),'lxml') 
nbd=str(bd).replace('<html><body><p>[</p><div class="list-recommend normal-recommend">\n','')
name=re.sub(r'.*<h3> <span><a href="/mtkj','mtkj',nbd)
print('测试')