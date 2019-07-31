import os
import sys
from jsonpickle import encode
from jsonpickle import decode
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from userdao import UserDao
from user import User
from feedDao import FeedDao
from workDao import WorkDao
from requestDao import RequestDao
from video import Video
from request import Request
from werkzeug import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
app = Flask(__name__)
#app.config['UPLOADS_DEFAULT_DEST'] = '/uploads'
#UPLOADS_DEFAULT_DEST = '/FinalProject/uploads/'
app.config['UPLOADS_FOLDER'] = './uploads'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    app.logger.debug('here is a debugging statement!!!')
    app.logger.debug('Hello, its Jerry!')    
    if request.method == 'POST':
        if isValid(request.form['userid'],request.form['password']):
            session['h1'] = "JER-SHARE"
            session['home'] = "HOME" 
            session['page'] = "workRequest.html"
            session['pageButton'] = "REQUEST"
            session['action'] = "workRequest"
            if(session['userid'] == "Jerry"):
                session['h1'] = "ADMINISTRATOR"
                session['home'] = "WELCOME JERRY"
                session['page'] = "viewRequest.html"
                session['pageButton'] = "REQUEST"
                session['action'] = "viewRequest"

            app.logger.debug(session['h1'])
            app.logger.debug(session['home'])
            app.logger.debug(session['pageButton'])
            app.logger.debug(session['action'])
            
            return redirect(url_for('home'))
        else:
            error = 'Invalid userid/password'
            
    return render_template('login.html', error=error)

@app.route('/home', methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

def isValid(userid, password):
    dao = UserDao()
    user = dao.selectByUserid(userid)
    if (user is not None) and (userid == user.userid) and (password == user.password):
        session['user']=encode(user)
        session['userid'] = user.userid

        return True
    else:
        return False

@app.route('/feed', methods = ['POST', 'GET'])
def feed():
    dao = FeedDao()
    feed = dao.table
    videos = []
    for row in feed:
        newVideo = dao.rowToVideo(row)
        newVideo.comments = decode(newVideo.comments)
        videos.append(newVideo)
        
    return render_template('feed.html', **locals())

@app.route('/work', methods = ['POST', 'GET'])
def work():
    dao = WorkDao(session['userid'])
    work = dao.table
    videos = []
    for row in work:
        newVideo = dao.rowToVideo(row)
        newVideo.comments = decode(newVideo.comments)
        videos.append(newVideo)
        
    return render_template('work.html', **locals())

@app.route('/like', methods = ['POST', 'GET'])
def like():
    if request.method == 'POST':
        name = request.form['name']
        name = name.replace("_", " ")
        app.logger.debug(name)
        
        dao = FeedDao()
        
        video = dao.selectByName(name)
        #app.logger.debug(video)
        video = dao.rowToVideo(video)
        app.logger.debug(video.userid)

        dao2 = WorkDao(video.userid)
        dao.like(name)
        dao2.like(video.name)

    return redirect(url_for('feed'))
@app.route('/comment', methods = ['POST', 'GET'])
def comment():
    if request.method == 'POST':
        userid = session['userid']
        name = request.form['name']
        comment = userid + ": "
        comment = comment + request.form['comment']
        name = name.replace("_", " ")
        dao = FeedDao()
        
        video = dao.selectByName(name)
        video = dao.rowToVideo(video)
        
        dao.addComment(name, comment)
        dao2 = WorkDao(video.userid)
        dao2.addComment(video.name, comment)
    return redirect(url_for('feed'))
@app.route('/deleteComment', methods = ['POST', 'GET'])
def deleteComment():
    if request.method == 'POST':
        name = request.form['name']
        name = name.replace("_", " ")
        app.logger.debug(name)
        comment = request.form['comment']
        comment = comment.replace("_", " ")
        dao = FeedDao()
        dao.removeComment(name, comment)

        video = dao.selectByName(name)
        video = dao.rowToVideo(video)
        dao2 = WorkDao(video.userid)
        dao2.removeComment(video.name, comment)
    return redirect(url_for('feed'))

@app.route('/deleteVideo', methods = ['POST', 'GET'])
def deleteVideo():
    if request.method == 'POST':
        name = request.form['name']
        name = name.replace("_", " ")
        app.logger.debug(name)
        dao = WorkDao(session['userid'])
        
        
        video = dao.selectByName(name)
        video = dao.rowToVideo(video)
        dao.delete(name)
        dao2 = FeedDao()
        dao2.delete(video.name)
    return redirect(url_for('work'))

@app.route('/createNew', methods = ['POST', 'GET'])
def createNew():
    if request.method == 'POST':
        app.logger.debug('hello')
        userid = request.form['userid']
        password = request.form['password']
        if(userid != "" and password != ""):
            user = User(userid, password)
            dao = UserDao()
            dao.insert(user)
            
        return redirect(url_for('login'))
    
    return render_template('createNew.html')

@app.route('/workRequest', methods = ['POST', 'GET'])
def workReqeust():
    return  render_template('workRequest.html')

@app.route('/newRequest', methods = ['POST', 'GET'])
def newRequest():
    if request.method == 'POST':
        userid = request.form['userid']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        title = request.form['title']
        desc = request.form['desc']
        app.logger.debug(userid)
        app.logger.debug(email)
        app.logger.debug(date)
        app.logger.debug(time)
        app.logger.debug(desc)
        newRequest = Request(userid, email, date, time, title, desc)
        dao = RequestDao()
        dao.insert(newRequest)
    return render_template('workRequest.html')

@app.route('/deleteRequest', methods = ['POST', 'GET'])
def deleteRequest():
    if request.method == 'POST':
        dao = RequestDao()
        title = request.form['title']
        title = title.replace("_", " ")
        dao.delete(title)
        
    return redirect(url_for('viewRequest'))
@app.route('/viewRequest', methods = ['POST', 'GET'])
def viewRequest():
    dao = RequestDao()
    rows = dao.table
    for row in rows:
        app.logger.debug(row['userid'])

    return render_template('viewRequest.html', **locals())
@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    return  render_template('upload.html')

@app.route('/uploader', methods = ['GET',  'POST'])
def upload_file():
    if request.method == 'POST':
        dao = FeedDao()
        dao2 = WorkDao(session['userid'])
        name = request.form['name']
        name = name
        app.logger.debug(name)
        rawname = "./static/uploads/"+name.replace(" ", "_")+".mp4"

        app.logger.debug(session['userid'])
        comments = []
        video = Video(name, rawname, session['userid'], "0", encode(comments))
        dao.insert(video)
        dao2.insert(video)
        f = request.files['file']
        f.save(os.path.join('./static/uploads', name.replace(" ", "_")+".mp4"))
        return render_template('upload.html')
    
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    streamhandler = logging.StreamHandler(sys.stderr)
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(Formatter("[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"))
    app.logger.addHandler(streamhandler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0')
