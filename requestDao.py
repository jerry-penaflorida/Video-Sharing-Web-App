import dataset
import logging
from request import Request
from flask import current_app
from jsonpickle import encode
from jsonpickle import decode
class RequestDao:
    def __init__(self):
        self.connectString = 'sqlite:///request.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['request']
        try:
            self.logger = current_app.logger
        except:
            self.logger = logging.getLogger('root')

    def insert(self, request):
        self.table.insert(self.requestToRow(request))
        self.db.commit()

    def requestToRow(self, request):
        row = dict(userid = request.userid, email = request.email, date = request.date, time = request.time, title = request.title,  desc = request.desc)
        return row

    def rowToRequest(self, row):
        video = Video(row['userid'], row['email'], row['date'], row['time'], row['title'], row['desc'])
        return video

    def selectAll(self):
        table = self.db['feed']
        rows = table.all()

        result = []
        for row in rows:
            result.append(self.rowToRequest(row))

        return result

    def delete(self, title):
        self.table.delete(title=title)
        self.db.commit()

    def selectByName(self, name):
        rows = self.table
        for row in rows:
            if(row['name']==name):
                return row
        #result = self.rowToVideo(row)

        #return result
        
