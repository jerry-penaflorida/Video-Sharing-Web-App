import dataset
import logging
from video import Video
from flask import current_app
from jsonpickle import encode
from jsonpickle import decode
class WorkDao:
    def __init__(self, userid):
        self.connectString = 'sqlite:///'+userid+'.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db[userid]
        try:
            self.logger = current_app.logger
        except:
            self.logger = logging.getLogger('root')

    def insert(self, video):
        self.table.insert(self.videoToRow(video))
        self.db.commit()

    def videoToRow(self, video):
        row = dict(name=video.name, rawname=video.rawname, userid=video.userid, likes=video.likes, comments=video.comments)
        return row

    def rowToVideo(self, row):
        video = Video(row['name'], row['rawname'], row['userid'], row['likes'], row['comments'])
        return video

    def selectAll(self):
        table = self.db['feed']
        rows = table.all()

        result = []
        for row in rows:
            result.append(self.rowToVideo(row))

        return result

    def delete(self, name):
        self.table.delete(name=name)
        self.db.commit()

    def selectByName(self, name):
        rows = self.table
        for row in rows:
            if(row['name']==name):
                return row
        #result = self.rowToVideo(row)

        #return result
        
    def like(self, name):
        video = self.rowToVideo(self.selectByName(name))
        likes = int(video.likes)
        likes = str(likes + 1)
        video.likes = likes
        self.table.update(self.videoToRow(video), ['name'])

    def addComment(self, name, comment):
        video = self.rowToVideo(self.selectByName(name))
        video.comments = decode(video.comments)
        video.comments.append(comment)
        video.comments = encode(video.comments)
        self.table.update(self.videoToRow(video), ['name'])
        
    def removeComment(self, name, comment):
        video = self.rowToVideo(self.selectByName(name))
        video.comments = decode(video.comments)
        video.comments.remove(comment)
        video.comments = encode(video.comments)
        self.table.update(self.videoToRow(video), ['name'])
