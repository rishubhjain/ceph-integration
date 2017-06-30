class Cluster():

    def __init__(self,*args,**kwargs):
        self.sync_status = ""
        self.last_sync = ""
        self.public_network = ""
        self.cluster_network = ""

    def save(self):
        pass

    def exists(self):
        return True

    def load(self):
        return self
