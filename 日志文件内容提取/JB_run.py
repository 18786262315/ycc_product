"""
提取java日志文件，定位接口测试数据，根据提取ngnix日志文件处理调整
"""

import os,sys,json,re
import pandas as pd

def extract(line):
    #正则提取并转换为字典
    #ngnix 正则  '''(?P<remote_addr>[\d\.]{7,}) - - (?:\[(?P<datetime>[^\[\]]+)\]) "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?:[^"]+)" "(?P<user_agent>[^"]+)"'''
    # java 日志文件 '''(?P<datetime>.*) (?:\[(?P<mm>.*)\]) (?P<res>[A-Z].*[A-Z]) (?P<ing>.*) -(?P<testss>[\u4e00-\u9fa5].*[\u4e00-\u9fa5])''' # [\u4e00-\u9fa5].*[\u4e00-\u9fa5] 中文
    pattern = '''(?P<datetime>.*) (?:\[(?P<mm>.*)\]) (?P<res>[A-Z].*[A-Z]) (?P<ing>.*) -(?P<testss>[\u4e00-\u9fa5].*[\u4e00-\u9fa5])''' 
    regex = re.compile(pattern)
    matcher = regex.match(line)
    return matcher


# red_file = ".\\API_test\\" # 日志文件所在文件夹
# file_list = os.listdir(red_file) # 获取当前文件夹下的所有文件，可以针对当前文件夹下的所有文件进行分别过滤
test_file = ".\\API_test\\app.log" #文件地址
files = open(test_file,'r',encoding='utf-8')
ip_d = [] # 统计结果
info = 0
debug = 0
warn=0
# for file_name in file_list:
#     # 循环整个文件夹，分别读取每个文件进行处理
#     # print(file_name)
#     if os.path.isfile(red_file + file_name):
#         print(file_name)
#         files = open(test_file,'r',encoding='utf-8')

for test in files.readlines():
    matcher = extract(test)
    if matcher :
        if matcher.groupdict()['res'] =="DEBUG":
            debug+=1
            if matcher.groupdict()['testss'] not in ["请求拦截","请求参数不合法",""]:
                ip_d.append(matcher.groupdict()['testss'])
        elif matcher.groupdict()['res'] =="INFO":
            if matcher.groupdict()['testss'] not in ["请求拦截","请求参数不合法",""]:
                ip_d.append(matcher.groupdict()['testss'])
            info+=1
        elif matcher.groupdict()['res'] =="WARN":
            warn+=1

print(info,debug,warn)
lists_jg = pd.value_counts(ip_d)
# print(type(lists_jg))
with open("test.txt",'w',encoding='utf-8') as tt:
    tt.write(str(lists_jg))










