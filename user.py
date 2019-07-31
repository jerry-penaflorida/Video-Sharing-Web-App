class User:
    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

    def toString(self):
        return self.userid + " " + self.password
