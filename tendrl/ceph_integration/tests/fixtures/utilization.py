import maps

class Utilization():

    def __init__(self,*args,**kwargs):
        pass

    def save(self):
        pass

    def exists(self):
        return True

class SyncObject():
    def __init__(self,*args,**kwargs):
         self.data = maps.NamedDict(public_network = "test",cluster_network = "test")

    def load(self):
        return self

class Osd():
    def __init__(self,*args,**kwargs):
         self.total = 0
         self.used = 0
         self.used_pcnt = 1

    def load(self):
        return self

    def save(self):
        pass
