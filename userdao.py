import dataset
import logging
from user import User
from flask import current_app

class UserDao:
    def __init__(self):
        self.connectString = 'sqlite:///users.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['users']
        try:
            self.logger = current_app.logger
        except:
            self.logger = logging.getLogger('root')
            
        self.logger.debug('got to UserDao')
        
    def rowToUser(self,row):
        user = User(row['userid'], row['password'])
        return user

    def userToRow(self,user):
        row = dict(userid=user.userid, password=user.password)
        return row

    def selectByUserid(self,userid):
        rows   = self.table.find(userid=userid)
        result = None
        if (rows is None):
            print('UserDao:selectByUserid failed to find user with ' + userid)
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
                    print('UserDao:selectByUserid more than one user selected with ' + userid)
                    return None
                else:
                    result = self.rowToUser(row)
                    count = count + 1

        return result

    def selectAll(self):
        table = self.db['users']
        rows   = table.all()

        result = []
        for row in rows:
            result.append(self.rowToUser(row))

        return result
        
    def insert(self,user):
        self.table.insert(self.userToRow(user))
        self.db.commit()

    def update(self,user):
        self.table.update(self.userToRow(user),['userid'])
        self.db.commit()

    def delete(self,user):
        self.table.delete(userid=userid)
        self.db.commit()

    def populate(self):
        self.table.insert(self.userToRow(User('bob','csrocks55')))
        self.table.insert(self.userToRow(User('ralph','csrocks55')))
        self.table.insert(self.userToRow(User('shai','csrocks55')))
        self.db.commit()
