import os
#获取需要合并的路径
meragefiledir = 'D:\\4-资料\\期货资料\\白糖\\2013'
#获取当前文件夹中的文件名称列表
filenames=os.listdir(meragefiledir)
#打开当前目录下的result.txt文件，如果没有则创建
#文件也可以是其他类型的格式，如result.js
file=open('result.txt','w',encoding='UTF-8')
#向文件中写入字符
#file.write('python\n')
 
#先遍历文件名
for filename in filenames:
    filepath=meragefiledir+'\\'+filename
    #遍历单个文件，读取行数
    for line in open(filepath,encoding='UTF-8'):
        file.writelines(line)
    file.write('\n\n\n\n---分隔符---\n')
 
#关闭文件
file.close()