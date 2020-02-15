import MySQLdb
import os
import datetime
# time=str(datetime.datetime.now())
# time=time[0:19]
# print(time)
# # os.mkdir("创建文件夹")
db = MySQLdb.connect("localhost", "root", "123456", "bilibili", charset='utf8' )
cursor = db.cursor()
cursor.execute("select * from danmakus where id='danmuidformiku7'")
danmakus=cursor.fetchall()
dict={}
dict['code']=0
dict['data']=[]
for i in danmakus:
    dict['data'].append(list(i))
# for i in comments[10:20]:
#     print(i)
# os.remove('static/banner.jpg')
print(dict)
# if av==None:
#     print("yes")
# print(av)
# av=eval(av[0])
# print(av)
# av+=1
# # cursor.execute("update data set value={} where name='av_num'".format(av))
# db.commit()
