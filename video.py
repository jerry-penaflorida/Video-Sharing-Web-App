class Video:
    def __init__(self, name, rawname, userid, likes, comments):
        self.name = name
        self.rawname = rawname
        self.userid = userid
        self.likes = likes
        self.comments = comments
    def toString(self):
        return self.name + " " + self.rawname + " " +  self.userid + " " + likes
