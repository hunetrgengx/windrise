contentbug=[]
j=1
while i<=len(mixinfo):
    try:
        for i in range(i,len(mixinfo)):
            target ='http://www.msweet.com.cn/'+mixinfo[i][1]
            req = requests.get(url=target)#requests获取请求
            req.encoding = 'utf-8'        #定义encoding
            html = req.text               #取req的属性
            bf = BeautifulSoup(html,'lxml')
            texts = bf.find_all('div', class_ = 'article')
            bd=BeautifulSoup(str(texts),'lxml') 
            text=bd.text.replace('[','').replace(']','')
            with open(r'E:\gj\研究\沐甜科技\\'+mixinfo[i][0]+'_'+re.search(r'\d\d\d\d-\d\d-\d\d',mixinfo[i][3],re.S).group()+'_'+mixinfo[i][2].replace(r'/','').replace(r'? ','')+".txt",'w',encoding='utf-8') as f:
                        f.writelines(mixinfo[i][2]+'\n'+mixinfo[i][3]+'\n'+'\n'+text) 
            print(i)    
    except :   
        if j<6:
            print('i=',i,'出错',j,'次')    
            j+=1
            time.sleep(3)   
        elif j>=6:
            urlbug.append(i)
            i+=1
            j=1 