class Cluster():

    def __init__(self,*args,**kwargs):
        self.sync_status = ""
        self.last_sync = ""

    def save(self):
        pass

    def exists(self):
        return True
