from flask import Flask,request,redirect,render_template,session,url_for,make_response,abort,flash
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
import os
import datetime
import  logging
import json,uuid

app=Flask(__name__)
app.secret_key=os.urandom(16)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/mikufans'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
# class User(db.Model):
#     uid = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), unique=True)
#     password =  db.Column(db.String(30))
#     email = db.Column(db.String(30))
#     phone = db.Column(db.String(15))
#     sex = db.Column(db.String(10))
#     sign = db.Column(db.String(100))
#     collection_movies = db.Column(db.String(1000))
#     movies = db.relationship('movie',backref='up')
#     comments = db.relationship('comment',backref='user')
#     def __init__(self,uid,username,password,sex):
#         self.username=username
#         self.uid=uid
#         self.password=password
#         self.sex=sex
#         self.email="23333@233.com"
#         self.phone="2333333"
#         self.sign="这个人很懒，他什么都没有写"
# class Movie(db.Model):
#     av_num = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(50))
#     up_id = db.Column(db.Integer,db.ForeignKey('user.uid'))
#     date = db.Column(db.String(30))
#     play = db.Column(db.Integer)
#     likes = db.Column(db.Integer)
#     collect = db.Column(db.Integer)
#     coins = db.Column(db.Integer)
#     danmaku = db.Column(db.Integer)
#     introduction = db.Column(db.String(100))
#     Class = db.Column(db.String(10))
#     tags = db.Column(db.String(100))
#     comments = db.relationship('comment',backref='movie')
#     def __int__(self,av_num,title,up_id,date,introduction,Class,tags):
#         self.av_num=av_num
#         self.title=title
#         self.up_id=up_id
#         self.date=date
#         self.introduction=introduction
#         self.Class=Class
#         self.tags=tags
#         self.play=0
#         self.likes=0
#         self.collect=0
#         self.coins=0
#         self.danmaku=0
# class Comment(db.Model):
#     rpid = db.Column(db.String(15),primary_key=True)
#     uid = db.Column(db.Integer,db.ForeignKey('user.uid'))
#     av = db.Column(db.Integer, db.ForeignKey('movie.av_num'))
#     content = db.Column(db.String(1000))
#     likes = db.Column(db.Integer)
#     date = db.Column(db.String(30))
#     def __init__(self,rpid,uid,av,content,date):
#         self.rpid=rpid
#         self.uid=uid
#         self.av=av
#         self.content=content
#         self.date=date
#         self.likes=0
# class data(db.Model):
#     name = db.Column(db.String(20),primary_key=True)
#     value = db.Column(db.Integer)
#     def __init__(self,name):
#         self.name=name
#         self.value=0
# db.create_all()
# av_num=data(name='av_num')
# comment_num=data('comment_num')
# user_num=data('user_num')
# db.session.add(av_num)
# db.session.add(comment_num)
# db.session.add(user_num)
# db.session.commit()

db = MySQLdb.connect("localhost", "root", "123456", "bilibili", charset='utf8' )
cursor = db.cursor()

fh=logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
app.logger.addHandler(fh)

@app.route('/')
def index():
    return render_template('index.html')

root="index"
@app.route('/login',methods=['POST','GET'])
def login():
    global root
    if request.method=='GET':
        root=request.headers['Referer']
        return render_template('login.html')
    else:
        username=str(request.form['uname'])
        passw=str(request.form['password'])

        #判断用户名是否存在
        cursor.execute("select name from user where name='{}'".format(username))
        u_exit=cursor.fetchone()
        # user=User.query.filter_by(username=username)
        if u_exit==None:
            flash("用户不存在")
            return redirect("login")

        #判断密码
        cursor.execute("select password,uid from user where name='{}'".format(username))
        info=cursor.fetchone()
        if(passw==info[0]):
            app.logger.info("'{}'登录成功".format(username))
            session['uname']=username
            session['uid']=info[1]
            referer=root
            root='index'
            if 'login' in referer:
                referer=url_for('index')
            return redirect(referer)
        else:
            app.logger.info("'{}'登录失败".format(username))
            flash("密码错误")
            return redirect("login")


@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method=='GET':
        return render_template('sign in.html')
    else:
        #验证
        if(request.form['password']!=request.form['passw_verify']):
            flash("两次密码输入不同")
            return render_template("sign in.html")

        #获取信息
        password=request.form['password']
        uname=request.form['uname']
        sex=request.form['sex']
        cursor.execute("select value from data where name='user_num'")
        uid=cursor.fetchone()
        # uid=data.query.filter_by(name='user_num').value
        uid=eval(uid[0])+1

        #判断用户名是否重复
        cursor.execute("select * from user where name='{}'".format(uname))
        name=cursor.fetchone()
        if name!=None:
            flash("该用户名已存在")
            return redirect(url_for('signin'))

        #更新数据库
        f = open("static/user/portrait/0.jpg", "rb")
        new = open("static/user/portrait/{}.jpg".format(uid), "wb")
        content = f.readlines()
        for i in content:
            new.write(i)
        f.close()
        new.close()
        f = open("static/user/space_cover/0.jpg", "rb")
        new = open("static/user/space_cover/{}.jpg".format(uid), "wb")
        content = f.readlines()
        for i in content:
            new.write(i)
        f.close()
        new.close()
        # user_new=User(uid,uname,password,sex)
        # db.session.add(user_new)
        # user_num=data.query.filter_by(name='user_num')
        # user_num.value=uid
        # db.session.commit()
        cursor.execute("insert into user ("
                       "name,password,uid,sex,phone,mail,sign)"
                       "values('{}','{}',{},'{}','无','无','无')".format(uname,password,uid,sex))
        cursor.execute("update data set value={} where name='user_num'".format(uid))

        db.commit()

        #设置会话
        session['uname']=uname
        session['uid']=uid
        app.logger.info("用户'{}'注册成功！".format(uname))
        return redirect(url_for('index'))


@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method=='GET':
        if 'uid' not in session:
            flash("请先登录")
            return redirect(url_for('login'))
        else:
            return render_template('upload.html')
    else:
        if 'uid' not in session:
            flash("会话超时，请先登录")
            return redirect(url_for('login'))
        #获取av号
        cursor.execute("select value from data where name='av_num';")
        av = cursor.fetchone()
        # av_num=data.query.filter_by(name='av_num')
        av = eval(av[0])+1
#分区数据库与用户数据库
        #更新movies表格
        movie=request.files['movie']
        cover=request.files['cover']
        movie.save('static/movies/movie/{}.mp4'.format(av))
        cover.save('static/movies/cover/{}.jpg'.format(av))
        time=str(datetime.datetime.now())[0:19]
        cursor.execute("insert into movies \
                       (date,up_name,up_id,av_num,play,likes,collect,coins,share,title,danmaku_num,introduction,tags,classes) \
                       values('{}','{}',{},{},0,0,0,0,0,'{}',0,'{}','{}','{}')".format(time,session['uname'],session['uid'],av,request.form['title'],request.form['introduction'],request.form['tags'],request.form['classes']))
        cursor.execute("update data set value={} where name='av_num'".format(av))
        db.commit()
        # movie_new=Movie(av,request.form['title'],session['uid'],time,request.form['introduction'],request.form['classes'],request.form['tags'])
        # db.session.add(movie_new)
        # av_num.value=av
        # db.session.commit()
        app.logger.info("用户'{}'上传视频“{}”成功，av{}".format(session['uname'],request.form['title'],av))
        return render_template("flash to index.html",info="上传")


@app.route('/logout')
def logout():
    app.logger.info('用户{}登出'.format(session['uname']))
    session.pop('uname',None)
    session.pop('uid',None)
    return render_template('flash to index.html',info='登出')


@app.route('/av<int:av>',methods=['POST','GET'])
def movie(av):
    if request.method=='GET':
        cursor.execute("select * from movies where av_num={}".format(av))
        info=cursor.fetchone()
        cursor.execute("select * from comments where av_num={} order by data desc".format(av))
        comments=cursor.fetchall()
        # movie=Movie.query.filter_by(av_num=av)
        pages=len(comments)
        if(pages%10==0):
            pages /= 10
        else:
            pages=int(pages/10)+1
        return render_template('movie.html',info=info,comments=comments,pages=int(pages))
    else:
        if 'uid' not in session:
            flash("请先登录")
            return redirect(url_for('login'))
        content=request.form['content']
        time = str(datetime.datetime.now())[0:19]
        cursor.execute("select value from data where name='comment_num';")
        rpid = cursor.fetchone()
        rpid = eval(rpid[0])
        rpid += 1
        cursor.execute("insert into comments\
                       (rpid,av_num,user_name,content,likes,data)\
                       values('{}',{},'{}','{}',0,'{}')".format(rpid,av,session['uname'],content,time))
        cursor.execute("update data set value={} where name='comment_num'".format(rpid))
        db.commit()
        return redirect(url_for('movie',av=av))


@app.route('/space/<int:uid>',methods=['POST','GET'])
def space(uid):
    if 'uid' not in session:
        flash("请先登录")
        return redirect(url_for("login"))
    if request.method=='GET':
        if int(session['uid']) != uid:
            return "无权限 <a href="+url_for('index')+">返回首页</a>"
        else:
            cursor.execute("select * from user where uid=" + str(session['uid']))
            info = cursor.fetchone()
            cursor.execute("select * from movies where up_name='{}';".format(session['uname']))
            movies_create = cursor.fetchall()
            movies_collect=getCollection(uid)
            cursor.execute("select * from comments where user_name='{}'".format(session['uname']))
            comments=cursor.fetchall()
            return render_template("space.html", info=info, movies_create=movies_create,movies_collect=movies_collect,comments=comments)
    else:
        if 'uid' not in session:
            flash("会话超时，请重新登录")
            return redirect("login")
        if request.form['uname'] != '空':
                cursor.execute("update user set name='{}' where uid={}".format(request.form['uname'],session['uid']))
        if request.form['sign'] != '空':
                cursor.execute("update user set sign='{}' where uid={}".format(request.form['sign'],session['uid']))
        if request.form['sex'] != '空':
                cursor.execute("update user set sex='{}' where uid={}".format(request.form['sex'], session['uid']))
        if request.form['tel'] != '空':
                cursor.execute("update user set phone='{}' where uid={}".format(request.form['tel'],session['uid']))
        if request.form['email'] != '空':
                cursor.execute("update user set mail='{}' where uid={}".format(request.form['email'],session['uid']))
        if request.form['passw'] != '空':
                cursor.execute("update user set password='{}' where uid={}".format(request.form['passw'],session['uid']))
        if request.files['portrait']:
                portrait=request.files['portrait']
                portrait.save("static/user/portrait/{}.jpg".format(session['uid']))
        db.commit()
        return redirect("/space/"+str(session['uid']))


@app.route('/v/<string:Class>')
def classes(Class):
    cursor.execute("select * from movies where classes='{}'".format(Class))
    movies=cursor.fetchall()
    pages = len(movies)
    if (pages % 5 == 0):
        pages /= 5
    else:
        pages = int(pages / 5) + 1
    return render_template("movie_list.html",movies=movies,pages=int(pages),Class=Class)


@app.route('/danmaku/v3/',methods=['POST','GET'])
def danmaku():
    if(request.method=='GET'):
        id=request.args['id']
        cursor.execute("select * from danmakus where id='{}'".format(id))
        danmakus=cursor.fetchall()
        dict={}
        dict['code']=0
        dict['data']=[]
        for i in danmakus:
            li = []
            li.append(i[4])
            li.append(i[5])
            li.append(i[3])
            li.append(i[6])
            li.append(i[2])
            dict['data'].append(li)
        return dict
    else:
        data = json.loads(request.get_data())
        cursor.execute("select dmid from danmakus order by dmid desc")
        dmid=cursor.fetchone()[0]+1
        author=data['author']
        color=data['color']
        type=data['type']
        id=data['id']
        text=data['text']
        time=data['time']
        cursor.execute("insert into danmakus set dmid={},author='{}',color={},type={},id='{}',text='{}',time={}".format(dmid,author,color,type,id,text,time))
        db.commit()

        msg = {
            "__v": 0,
            "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data["type"],
            "ip": request.remote_addr,
            "player": data["id"]
        }
        res = {
            "code": 0,
            "danmaku": msg
        }
        resp = make_response(json.dumps(res))
        resp.headers['ontent-type']="application/json"
        return resp


@app.route('/update_like',methods=['POST'])
def update_like():
    rpid = request.form['rpid']
    if 'uid' not in session:
        return "请先登录"
    cursor.execute("select likes from comments where rpid={}".format(rpid))
    likes_now=cursor.fetchone()
    likes_now=likes_now[0]
    cursor.execute("update comments set likes={} where rpid={};".format(int(likes_now)+1,rpid))
    db.commit()
    return str(int(likes_now)+1)


@app.route('/update_like_movie',methods=['POST'])
def update_like_movie():
    if 'uid' not in session:
        return " 请先登录"
    av=request.form['av']
    cursor.execute("select likes from movies where av_num={}".format(av))
    likes_now=cursor.fetchone()
    likes_now=likes_now[0]
    cursor.execute("update movies set likes={} where av_num={};".format(int(likes_now)+1,av))
    db.commit()
    return str(int(likes_now)+1)


@app.route('/update_collection',methods=['POST'])
def update_collection():
    if 'uid' not in session:
        return " 请先登录"
    av=request.form['av']
    cursor.execute("select collect from movies where av_num={}".format(av))
    likes_now = cursor.fetchone()
    likes_now = likes_now[0]

    cursor.execute("select collection_movies from user where uid={};".format(session['uid']))
    collection = cursor.fetchone()
    collection = collection[0]
    if collection==None:
        collection=""
    if str(av) in collection:
        return " 你个笨蛋你已经收藏过了"
    collection += str(av)+","
    cursor.execute("update user set collection_movies='{}' where uid={}".format(collection,session['uid']))
    cursor.execute("update movies set collect={} where av_num={};".format(int(likes_now) + 1, av))
    db.commit()
    return str(int(likes_now)+1)


@app.route('/update_play',methods=['POST'])
def update_play():
    av=request.form['av']
    cursor.execute("select play from movies where av_num={}".format(av))
    likes_now = cursor.fetchone()
    likes_now = likes_now[0]
    cursor.execute("update movies set play={} where av_num={};".format(int(likes_now) + 1, av))
    db.commit()
    return str(int(likes_now)+1)


@app.route('/update_danmaku',methods=['POST'])
def update_danmaku():
    av=request.form['av']
    cursor.execute("select danmaku_num from movies where av_num={}".format(av))
    likes_now = cursor.fetchone()
    likes_now = likes_now[0]
    cursor.execute("update movies set danmaku_num={} where av_num={};".format(int(likes_now) + 1, av))
    db.commit()
    return str(int(likes_now)+1)


@app.route('/change_page',methods=['POST'])
def change_page():
    page=request.form['page']
    page=int(page)
    movie=request.form['movie']
    cursor.execute("select * from comments where av_num={} order by data desc".format(movie))
    comments = cursor.fetchall()
    content={'user':[],'text':[],'data':[],'likes':[],"rpid":[]}
    cnt=0
    for i in comments[(page-1)*10:page*10]:
        content['user'].append(i[2])
        content['text'].append(i[3])
        content['data'].append(i[5])
        content['likes'].append(i[4])
        content['rpid'].append(i[0])
        cnt+=1
    content['num']=str(cnt)
    resp=""
    for i in range(0,cnt):
        if 'uid' in session and session['uid']==1:
            resp=resp+"<div class=\"comment\" id=\"comment_"+content['rpid'][i]+"\">\
                            <div class=\"name\">user:"+content['user'][i]+"</div>\
                            <div class=\"content\">"+content['text'][i]+"</div>\
                            <div class=\"op\">\
                                <span>"+str(content['data'][i])+"</span>\
                                <span><span onclick=\"update_like("+str(content['rpid'][i])+")\">点赞</span><span id=\"likes_"+str(content['rpid'][i])+"\">"+str(content['likes'][i])+"</span></span>\
                                <a onclick=\"del("+content['rpid'][i]+",'pl')\">删除</a>\
                            </div>\
                        </div>"
        else:
            resp = resp + "<div class=\"comment\" id=\"comment_"+content['rpid'][i]+"\">\
                                        <div class=\"name\">user:" + content['user'][i] + "</div>\
                                        <div class=\"content\">" + content['text'][i] + "</div>\
                                        <div class=\"op\">\
                                            <span>" + str(content['data'][i]) + "</span>\
                                            <span><span onclick=\"update_like(" + str(
                content['rpid'][i]) + ")\">点赞</span><span id=\"likes_" + str(content['rpid'][i]) + "\">" + str(
                content['likes'][i]) + "</span></span>\
                                        </div>\
                                    </div>"

    return resp


@app.route('/change_page_class',methods=['POST'])
def change_page_class():
    page=request.form['page']
    page=int(page)
    Class=request.form['Class']
    cursor.execute("select * from movies where classes='{}' order by play desc,date desc".format(Class))
    info = cursor.fetchall()
    content={'up':[],'title':[],'av':[],'likes':[],"collect":[],'play':[],'danmaku':[],'text':[]}
    cnt=0
    for i in info[(page-1)*5:page*5]:
        content['up'].append(i[1])
        content['text'].append(i[15])
        content['likes'].append(i[5])
        content['av'].append(i[0])
        content['play'].append(i[4])
        content['collect'].append(i[6])
        content['danmaku'].append(i[13])
        content['title'].append(i[9])
        cnt+=1
    resp=""
    for i in range(0,cnt):
        if 'uid' in session and session['uid']==1:
            resp=resp+"<div class=\"card_movies\" id=\"movie_"+str(content['av'][i])+"\">\
                    <div class=\"movie_card_left\"><a href="+url_for('movie',av=content['av'][i])+" target=\"_blank\"><img src="+url_for('static',filename="movies/cover/{}.jpg".format(content['av'][i]))+"></a></div>\
                    <div class=\"movie_card_right\">\
                        <div class=\"card_title\"><a href="+url_for('movie',av=str(content['av'][i]))+" target=\"_blank\"><strong>"+content['title'][i]+"</strong></a></div>\
                        <div class=\"card_info\">\
                            <div>up:"+content['up'][i]+")</div>\
                            <div>\
                                <span>播放："+str(content['play'][i])+"</span>\
                                <span>弹幕："+str(content['danmaku'][i])+"</span>\
                                <span>点赞："+str(content['likes'][i])+"</span>\
                                <span>收藏："+str(content['collect'][i])+"</span>\
                                <a onclick=\"del("+str(content['av'][i])+",'sp')\">删除</a>\
                            </div>\
                        </div>\
                        <div class=\"card_intro\">"+str(content['text'][i])+"</div>\
                    </div>\
                </div>"
        else:
            resp = resp + "<div class=\"card_movies\" id=\"movie_" + str(content['av'][i]) + "\">\
                                <div class=\"movie_card_left\"><a href=" + url_for('movie', av=content['av'][i]) + " target=\"_blank\"><img src=" + url_for('static', filename="movies/cover/{}.jpg".format(content['av'][i])) + "></a></div>\
                                <div class=\"movie_card_right\">\
                                    <div class=\"card_title\"><a href=" + url_for('movie', av=str(content['av'][i])) + " target=\"_blank\"><strong>" + content['title'][i] + "</strong></a></div>\
                                    <div class=\"card_info\">\
                                        <div>up:" + content['up'][i] + ")</div>\
                                        <div>\
                                            <span>播放：" + str(content['play'][i]) + "</span>\
                                            <span>弹幕：" + str(content['danmaku'][i]) + "</span>\
                                            <span>点赞：" + str(content['likes'][i]) + "</span>\
                                            <span>收藏：" + str(content['collect'][i]) + "</span>\
                                        </div>\
                                    </div>\
                                    <div class=\"card_intro\">" + str(content['text'][i]) + "</div>\
                                </div>\
                            </div>"
    return resp


@app.route('/delete',methods=['POST'])
def delete():
    obj=request.form['obj'];
    index=request.form['index']
    if(obj=='pl'):
        cursor.execute("delete from comments where rpid="+index)
    else:
        cursor.execute("delete from movies where av_num="+index)
        os.remove('static/movies/cover/{}.jpg'.format(index))
        os.remove('static/movies/movie/{}.mp4'.format(index))
    db.commit()
    app.logger.info('用户"{}" 删除{} id={}'.format(session['uname'],obj,index))
    return "1"


def getCollection(uid):
    cursor.execute("select collection_movies from user where uid={};".format(uid))
    collection = cursor.fetchone()
    collection = collection[0]
    movies_collect = []
    if collection != None:
        collection = collection.split(',')
    else:
        return movies_collect
    for i in collection:
        if i != '':
            cursor.execute("select * from movies where av_num={}".format(i))
            a=cursor.fetchone()
            if a!=None:
                movies_collect.append(a)
    return movies_collect

app.run(debug=True)