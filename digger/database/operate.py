from database import SESSION

class operateDb:
    def __init__(self):
        self.session = SESSION()
    def add(self,object):
        self.session.add(object)
        self.session.commit()
    def addmany(self,objectlist):
        self.session.add_all(objectlist)
        self.session.commit()
    def filterone(self,object,filter):
        return self.session.query(object).filter(filter).first()

    def update(self,object,filter,updic):
        self.session.query(object).filter(filter).update(updic)
        self.session.commit()
