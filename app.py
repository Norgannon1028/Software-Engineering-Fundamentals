from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session,jsonify,current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from sqlalchemy import and_, or_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import re
import datetime,time
from threading import Thread
import random
import string
import base64

app = Flask(__name__,template_folder="src/views",static_folder='./src/assets/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)


#Mail config
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''
mail = Mail(app)
############################################
# 数据库
############################################

# 定义ORM
# User类把我们刚刚创建的几个字段定义为类变量。
# 字段使用db.Column类创建实例，字段的类型作为参数，另外还提供一些其他可选参数
# __repr__方法告诉Python如何打印class对象，方便我们调试使用
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(20), unique=True)
    sex = db.Column(db.String(10))
    old = db.Column(db.Integer)
    time = db.Column(db.String(80))
    avatar = db.Column(db.TEXT)

    def __repr__(self):
        return '<User %r>' % self.username
    def to_dict(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def generate_auth_token(self,expiration):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in = expiration)
        return  s.dumps({'id':self.id,'name':self.username,'avatar':self.avatar}).decode('utf-8')
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
        
class Blog(db.Model):
    __tablename__='Blog'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    keyword = db.Column(db.String(80))
    like = db.Column(db.Integer)
    link = db.Column(db.Text, unique=True)
    title = db.Column(db.String(80))
    time = db.Column(db.String(80))

    def to_json(self):
        return jsonify(self.to_dict)
    def to_dict(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    def __repr__(self):
        return '<Info %r>' % self.id

class File(db.Model):
    __tablename__='File'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer),
    filename=db.Column(db.Text),
    link = db.Column(db.String(80)),
    time = db.Column(db.String(80))

    def __repr__(self):
        return '<Info %r>' % self.username

class Follow(db.Model):
    __tablename__='Follow'
    id = db.Column(db.Integer, primary_key=True)
    toid = db.Column(db.Integer)
    fromid = db.Column(db.Integer)

    def __repr__(self):
        return '<Info %r>' % self.username

class Comment(db.Model):
    __tablename__='Comment'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    blogid = db.Column(db.Integer)
    content = db.Column(db.String(80))
    time = db.Column(db.String(80))

    def __repr__(self):
        return '<Info %r>' % self.content
    def to_dict(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

class Like(db.Model):
    __tablename__='Like'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    blogid = db.Column(db.Integer)
    time = db.Column(db.String(80))

    def __repr__(self):
        return '<Info %r>' % self.username
class Draft(db.Model):
    __tablename__='Draft'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    keyword = db.Column(db.String(80))
    link = db.Column(db.Text, unique=True)
    title = db.Column(db.String(80))
    time = db.Column(db.String(80))

    def to_json(self):
        return jsonify(self.to_dict)
    def to_dict(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    def __repr__(self):
        return '<Info %r>' % self.id
# 创建表格、插入数据
@app.before_first_request
def create_db():
    db.create_all()
    #admin = User(username='admin', password='root', email='admin@example.com')
    #db.session.add(admin)

    #guestes = [User(username='guest1', password='guest1', email='guest1@example.com'),
    #           User(username='guest2', password='guest2', email='guest2@example.com'),
    #           User(username='guest3', password='guest3', email='guest3@example.com'),
    #           User(username='guest4', password='guest4', email='guest4@example.com')]
    #db.session.add_all(guestes)
    db.session.commit()
    

############################################
# 辅助函数、装饰器
############################################

# 登录检验（用户名、密码验证）
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False

def valid_regist(username, password1, password2, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:
        return False
    else:
        return True

#发送邮件(异步)
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)
 
def send_async_mail(subject, to ,body):
    message = Message(subject, recipients=[to],body=body)
    thread = Thread(target=_send_async_mail, args=[app, message])
    thread.start()
    return thread
#发送邮件(同步)
def send_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)


def return_img_stream(img_local_path):
    img_stream = ''
    with open(img_local_path, 'rb') as f:
        res = base64.b64encode(f.read())
    return res

############################################
# 路由
############################################

# 1.主页
@app.route('/')
# def home():
#     return render_template('Home.vue', username=session.get('username'))

# 2.登录
@app.route('/signin', methods=['GET', 'POST'])
def login():
    response={}
    error = None
    thispeopleid=0
    token=""
    message='测试'
    if request.method == 'POST':
        j_data=request.json
        uname=j_data.get("username")
        p=j_data.get("password")
        print(uname)
        print(p)
        if valid_login(uname, p):
            message='登录成功!' 
            thispeople=User.query.filter(User.username==uname).first()
            thispeopleid=thispeople.id
            token=thispeople.generate_auth_token(expiration=3600)
        else:
            message='用户名或密码错误!'
    response={'msg':message,'id':thispeopleid,'token':token}
    print(response)
    return jsonify(response)

# 3.注册
@app.route('/regist', methods=['GET','POST'])
def regist():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        uname=j_data.get("username")
        p1=j_data.get("password1")
        p2=j_data.get("password2")
        em=j_data.get("email")
       # print(em,uname)
        if valid_regist(uname, p1, p2, em):
            today = datetime.date.today()
            user=User(username=uname, password=p1, email=em, sex="1", old="18", time=today,avatar="http://127.0.0.1:5000/static/default_avatar.jpg")
            db.session.add(user)
            db.session.commit()
            message='注册成功!'
        else:
            message='用户名或邮箱重复!'
    response={'msg':message}
    print(response)
    return jsonify(response)

# 4.读取用户个人信息
@app.route('/getinfo', methods=['GET','POST'])
def getinfo():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        uname=j_data.get("username")
        info = User.query.filter(User.username == uname).first()
        userid = info.id
        fansnum=db.session.query(Follow).filter(Follow.toid==userid).count()
        follownum=db.session.query(Follow).filter(Follow.fromid==userid).count()
    response={
         'name':info.username,
         'face':info.avatar,
         'sex':info.sex,
         'old':info.old,
         'email':info.email,
         'fansnum':fansnum,
         'follownum':follownum
    }    
    #print(response.old)
    print(response)
    return jsonify(response)

#重置密码
@app.route('/repassword', methods=['GET','POST'])
def repassword():
    response={}
    error = None
    message=''
    if request.method == 'POST':
        j_data=request.json
        username=j_data.get("username")
        email=j_data.get("email")
        user = User.query.filter(and_(User.username == username)).first()
        if user==None:
            message='用户不存在！'
            print(message)
        elif user.email!=email:
            message='邮箱错误，请输入注册时的邮箱！'
            print(message)
        else:
            pwd = ""
            letters=string.ascii_letters+string.digits
            for i in range(10):
                letter=random.choice(letters)
                pwd += letter
            tmp = User.query.filter(User.username == username).update({"password":pwd})
            db.session.commit()
            try:
                send_mail("技术分享博客网站账户重置密码",email,"重置密码:"+pwd+",请及时修改密码")
                message= '新的密码已经发至您的邮箱，请注意查收并及时修改～'
            except Exception as e:
                print(e)
                message='邮件发送失败，请稍后重试'
    response={
         'message':message
    }    
    print(response)
    return jsonify(response)

#修改密码
@app.route('/changepassword', methods=['GET','POST'])
def changepassword():
    response={}
    error = None
    message=''
    if request.method == 'POST':
        j_data=request.json
        username=j_data.get("username")
        oldpassword=j_data.get("oldpassword")
        newpasswprd=j_data.get("password")
        user = User.query.filter(User.username == username).first()
        print(user.password)
        print(oldpassword)
        if user == None:
            message='用户不存在！'
        elif user.password != oldpassword:
            message='旧密码错误！'
        else:
            tmp = User.query.filter(User.username == username).update({"password":newpasswprd})
            db.session.commit()
            message='密码修改成功！'
    response={
         'msg':message
    }    
    print(response)
    return jsonify(response)


#更新用户个人信息
@app.route('/info', methods=['GET','POST'])
def info():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        uname=j_data.get("username")
        age=j_data.get("age")
        sex=j_data.get("sex")
        avatar=j_data.get("avatar")
        print(avatar)
        user = User.query.filter(User.username == uname).first()
        if user!=None:
            user.old=age
            user.sex=sex
            user.avatar=avatar
            response={"token":user.generate_auth_token(3600)}
        db.session.commit()
    return response

#发送安全代码验证邮件
@app.route('/verification', methods=['GET','POST'])
def verify():
    response={}
    error = None
    message=''
    if request.method == 'POST':
        j_data=request.json
        code=j_data.get("code")
        email=j_data.get("email")
        print(code)
        print(email)
        try:
            send_mail("安全代码",email,"安全代码:"+str(code))
            message= '发送成功，请注意查收~'
        except Exception as e:
            print(e)
            message='发送失败，请稍后重试'
    response={
         'message':message
    }    
    print(response)
    return jsonify(response)

#主页推荐博客
@app.route('/recommend', methods=['GET','POST'])
def recommend():
    response={}
    result = []
    error = None
    blogs = None
    if request.method == 'POST':
        i=1
        j_data=request.json
        recommendway=str(j_data.get("recommendway"))
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        if recommendway == '最新':
            blogs=db.session.query(Blog).join(User, User.id==Blog.userid).order_by(Blog.time.desc())
        elif recommendway == '最热门':
            blogs=db.session.query(Blog).join(User, User.id==Blog.userid).order_by(Blog.like.desc())
        print(blogs)
        for blog in blogs:
            if blog == None:
                continue
            tmp=User.query.filter(User.id == blog.userid).first()
            #print(tmp.username)
            blog=blog.to_dict()
            blog['userid']=tmp.username
            blog['face']=tmp.avatar
            #blog['id']=tmp.avatar
            #print(blog)
            response['blog'+str(i)]=blog
            i+=1
            #result.append(blog.to_json())
    print(response)
    return jsonify(response)

#主页搜索博客
@app.route('/searchblog', methods=['GET','POST'])
def searchblog():
    response={}
    result = []
    error = None
    blogs = None
    if request.method == 'POST':
        i=1
        j_data=request.json
        searchkey=j_data.get("searchkey")
        searchway=j_data.get("searchway")
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        if searchway == '最新':
            blogs=db.session.query(Blog).join(User, User.id==Blog.userid).filter(or_(Blog.title.like('%'+searchkey+'%'),User.username.like('%'+searchkey+'%'))).order_by(Blog.time.desc())
        elif searchway == '最热门':
            blogs=db.session.query(Blog).join(User, User.id==Blog.userid).filter(or_(Blog.title.like('%'+searchkey+'%'),User.username.like('%'+searchkey+'%'))).order_by(Blog.like.desc())
        for blog in blogs:
            if blog == None:
                continue
            tmp=User.query.filter(User.id == blog.userid).first()
            #print(tmp.username)
            blog=blog.to_dict()
            blog['userid']=tmp.username
            blog['face']=tmp.avatar
            #print(blog)
            response['blog'+str(i)]=blog
            i+=1
            #result.append(blog.to_json())
    print(response)
    return jsonify(response)


#新建博客
@app.route('/write', methods=['GET','POST'])
def writeblog():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        userid=j_data.get("userid")
        md=j_data.get("md")
        title=j_data.get("title")
        keyword=j_data.get("keyword")
        draftid=j_data.get("draftid")
        blog=Blog(userid=userid,keyword=keyword,title=title,link=md,like=0,time=time.strftime("%Y-%m-%d",time.localtime(time.time())))
        db.session.add(blog)
        draft=db.session.query(Draft).filter(Draft.id==draftid).first()
        print(draftid)
        if draft != None:
            db.session.delete(draft)
        db.session.commit()
        message='发布成功!'
    response={'msg':message}
    print(response)
    return jsonify(response)
    
#用户信息页面userid对应的所有博客
@app.route('/allhisblog', methods=['GET','POST'])
def allhisblog():
    response={}
    result = []
    error = None
    blogs = None
    if request.method == 'POST':
        i=1
        j_data=request.json
        username=j_data.get("username")
        user=User.query.filter(User.username == username).first()
        userid=user.id
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        blogs=Blog.query.filter(Blog.userid==userid).order_by(Blog.time.desc(),Blog.id.desc())
        for blog in blogs:
            if blog == None:
                continue
            tmp=User.query.filter(User.id == blog.userid).first()
            if tmp==None:
                continue
            #print(tmp.username)
            blog=blog.to_dict()
            blog['userid']=tmp.username
            blog['face']=tmp.avatar
            #print(blog)
            response['blog'+str(i)]=blog
            i+=1
            #result.append(blog.to_json())
    print(response)
    return jsonify(response)


#加载推荐的博客评论
@app.route('/loadcomments', methods=['GET','POST'])
def loadcomments():
    response={}
    result = []
    error = None
    comments = None
    if request.method == 'POST':
        i=0
        j_data=request.json
        blogid=j_data.get("blogid")
        comments=Comment.query.filter(Comment.blogid==blogid).order_by(Comment.time.desc(),Comment.id.desc())
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        print(comments)
        for comment in comments:
            if comment == None:
                continue
            id=int(comment.userid)
            tmp=User.query.filter(User.id == id).first()
            if tmp==None:
                continue
            print(tmp)
            comment=comment.to_dict()
            comment['userid']=tmp.username
            comment['face']=tmp.avatar
            #print(blog)
            response['comment'+str(i)]=comment
            i+=1
            if i == 3:
                break
            #result.append(blog.to_json())
    print(response)
    return jsonify(response)

#保存草稿
@app.route('/savedraft', methods=['GET','POST'])
def savedraft():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        userid=j_data.get("userid")
        draftid=j_data.get("draftid")
        md=j_data.get("md")
        title=j_data.get("title")
        keyword=j_data.get("keyword")
        print(j_data)
        if draftid==0:
            draft=Draft(userid=userid,keyword=keyword,title=title,link=md,time=time.strftime("%Y-%m-%d",time.localtime(time.time())))
            db.session.add(draft)
            db.session.commit()
        else:
            draft=Draft.query.filter(and_(Draft.userid==userid,Draft.id==draftid)).first()
            if draft != None:
                draft.title=title
                draft.link=md
                draft.keyword=keyword
                db.session.commit()
        message='保存草稿成功!'
    response={'msg':message}
    print(response)
    return jsonify(response)
#获得草稿
@app.route('/getdraft', methods=['GET','POST'])
def getdraft():
    response={}
    error = None
    draft_flag=False
    if request.method == 'POST':
        j_data=request.json
        print(j_data)
        userid=j_data.get("userid")
        draftid=j_data.get("draftid")
        draft=Draft.query.filter(and_(Draft.userid==userid,Draft.id==draftid)).first()
        if draft != None:
            draft_flag=True
            message='读取草稿成功!'
            response={'msg':message,
            'draft':draft.to_dict(),
            'draft_flag':draft_flag}
        else:
            message='读取草稿失败!'
            response={'msg':message,
            'draft':'null',
            'draft_flag':draft_flag}
    print(response)
    return jsonify(response)

#全部草稿
@app.route('/getalldraft', methods=['GET','POST'])
def getalldraft():
    response={}
    result = []
    error = None
    if request.method == 'POST':
        i=1
        j_data=request.json
        userid=j_data.get("userid")
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        drafts=db.session.query(Draft).filter(Draft.userid==userid).all()
        for draft in drafts:
            if draft == None:
                continue
            draft=draft.to_dict()
            response['draft'+str(i)]=draft
            i+=1
    print(response)
    return jsonify(response)

#新建评论
@app.route('/addcomment', methods=['GET','POST'])
def addcomment():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        userid=j_data.get("thisuser")
        text=j_data.get("commenttext")
        blogid=j_data.get("blogid")
        print(time.strftime("%Y-%m-%d",time.localtime(time.time())))
        comment=Comment(userid=userid,blogid=blogid,content=text,time=time.strftime("%Y-%m-%d",time.localtime(time.time())))
        print(comment)
        db.session.add(comment)
        db.session.commit()
        message='评论成功！'
    response={'msg':message}
    print(response)
    return jsonify(response)

#全部评论
@app.route('/allcomments', methods=['GET','POST'])
def allcomments():
    response={}
    result = []
    error = None
    comments = None
    if request.method == 'POST':
        i=1
        j_data=request.json
        blogid=j_data.get("blogid")
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        comments=db.session.query(Comment).filter(Comment.blogid==blogid).order_by(Comment.time.desc(),Comment.id.desc()).all()
        print(comments)
        for comment in comments:
            if comment == None:
                continue
            tmp=User.query.filter(User.id == comment.userid).first()
            #print(tmp.username)
            if tmp == None:
                continue 
            comment=comment.to_dict()
            comment['userid']=tmp.username
            #print(blog)
            response['comment'+str(i)]=comment
            i+=1
            #result.append(blog.to_json())
    print(response)
    return jsonify(response)
    
#添加点赞
@app.route('/addlike', methods=['GET','POST'])
def addlike():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        blogid=j_data.get("blogid")
        thisuserid=j_data.get("thisuser")
        blog = Blog.query.filter(Blog.id == blogid).first()
        tmp = Blog.query.filter(Blog.id == blogid).update({"like":blog.like+1})
        like=Like(userid=thisuserid,blogid=blogid,time=time.strftime("%Y-%m-%d",time.localtime(time.time())))
        db.session.add(like)
        db.session.commit()
        message='点赞成功！'
    response={
        'msg':message,
    }
    print(response)
    return jsonify(response)

#取消点赞
@app.route('/dislike', methods=['GET','POST'])
def dislike():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        blogid=j_data.get("blogid")
        thisuserid=j_data.get("thisuser")
        blog = Blog.query.filter(Blog.id == blogid).first()
        tmp = Blog.query.filter(Blog.id == blogid).update({"like":blog.like-1})
        like = Like.query.filter(and_(Like.userid == thisuserid,Like.blogid == blogid)).first()
        db.session.delete(like)
        db.session.commit()
        message='已取消点赞！'
    response={
        'msg':message,
    }
    print(response)
    return jsonify(response)


#全部关注者
@app.route('/allfollows', methods=['GET','POST'])
def allfollows():
    response={}
    result = []
    error = None
    if request.method == 'POST':
        i=1
        j_data=request.json
        username=j_data.get("username")
        user=User.query.filter(User.username==username).first()
        userid=user.id
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        follows=db.session.query(Follow).filter(Follow.fromid==userid).all()
        for follow in follows:
            followerid=follow.fromid
            follower=User.query.filter(User.id==followerid).first()
            follower=follower.to_dict()
            response['follower'+str(i)]=follower
            i+=1
    print(response)
    return jsonify(response)

#全部粉丝
@app.route('/allfans', methods=['GET','POST'])
def allfans():
    response={}
    result = []
    error = None
    if request.method == 'POST':
        i=1
        j_data=request.json
        username=j_data.get("username")
        user=User.query.filter(User.username==username).first()
        userid=user.id
        #print(db.session.query(Blog).join(User, User.id==Blog.userid))
        follows=db.session.query(Follow).filter(Follow.toid==userid).all()
        for follow in follows:
            fansid=follow.fromid
            fans=User.query.filter(User.id==fansid).first()
            fans=fans.to_dict()
            response['fans'+str(i)]=fans
            i+=1
    print(response)
    return jsonify(response)

#检查关注
@app.route('/checkfollow', methods=['GET','POST'])
def checkfollow():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        myname=j_data.get("myname")
        hisname=j_data.get("hisname")
        my=User.query.filter(User.username==myname).first()
        he=User.query.filter(User.username==hisname).first()
        myid=my.id
        hisid=he.id
        follow=Follow.query.filter(and_(Follow.toid==hisid,Follow.fromid==myid)).first()
        if follow == None:
            followflag=False
        else:
            followflag=True
    response={
        'followflag':followflag
    }    
    print(response)
    return jsonify(response)

#添加关注
@app.route('/followhim', methods=['GET','POST'])
def followhim():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        myname=j_data.get("myname")
        hisname=j_data.get("hisname")
        my=User.query.filter(User.username==myname).first()
        he=User.query.filter(User.username==hisname).first()
        myid=my.id
        hisid=he.id
        follow=Follow(toid=hisid,fromid=myid)
        db.session.add(follow)
        db.session.commit()
        message='关注成功！'
    response={
        'msg':message,
    }
    print(response)
    return jsonify(response)

#取消关注
@app.route('/disfollowhim', methods=['GET','POST'])
def disfollowhim():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        myname=j_data.get("myname")
        hisname=j_data.get("hisname")
        my=User.query.filter(User.username==myname).first()
        he=User.query.filter(User.username==hisname).first()
        myid=my.id
        hisid=he.id
        follow = Follow.query.filter(and_(Follow.fromid == myid,Follow.toid == hisid)).first()
        db.session.delete(follow)
        db.session.commit()
        message='取消关注成功！'
    response={
        'msg':message,
    }
    print(response)
    return jsonify(response)

#获得博客
@app.route('/getblog', methods=['GET','POST'])
def getblog():
    response={}
    error = None
    if request.method == 'POST':
        j_data=request.json
        id=j_data.get("blogid")
        thisuserid=j_data.get("thisuser")
        print("hi")
        print(id)
        print("hi")
        blog=Blog.query.filter(Blog.id==id).first()
        userid=blog.userid
        user=User.query.filter(User.id==userid).first()
        like=Like.query.filter(and_(Like.userid==thisuserid,Like.blogid==blog.id)).first()
        retblog=blog.to_dict()
        if like == None:
            likeflag=False
        else:
            likeflag=True
    response={
        'face':user.avatar,
        'blog':retblog,
        'writer':user.username,
        'likeflag':likeflag
    }    
    print(response)
    return jsonify(response)

#上传头像
@app.route('/uploadavatar', methods=['GET','POST'])
def up_photo():
    if request.method != 'POST':
        print("not post")
        return
    print(request.data)
    print(request.form)
    print(request.files)
    img = request.files.get('file')
    path = "./src/assets/static/"
    file_path = path+img.filename
    img.save(file_path)
    print('上传头像成功，上传的用户是：')
    response={
         'image_url':'http://127.0.0.1:5000/static/'+img.filename,
         'code':0
    } 
    print(response)
    return jsonify(response)
    
#上传文件
@app.route('/uploadfile', methods=['GET','POST'])
def up_file():
    file = request.files.get('file')
    id=int(request.form["userid"])
    print(id)
    path = "./src/assets/static/"
    file_path = path+file.filename
    file.save(file_path)
    print('上传文件成功，上传的用户是：')
    file_link='http://127.0.0.1:5000/static/'+file.filename
    if id>0:
        f=File(userid=1,filename=file.filename,link=file_link,time=time.strftime("%Y-%m-%d",time.localtime(time.time()))) 
        db.session.add(f)
        db.session.commit()
        response={
            'userid':id,
            'file_url':'http://127.0.0.1:5000/static/'+file.filename,
            'code':0
        }
    else:
     response={
            'code':1
        }
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug = True)
