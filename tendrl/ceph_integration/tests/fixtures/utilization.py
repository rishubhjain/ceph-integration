import maps


class Utilization:

    def __init__(self,*args,**kwargs):
        pass

    def save(self):
        pass

    def exists(self):
        return True


class SyncObject:
    def __init__(self,*args,**kwargs):
         self.data = maps.NamedDict(public_network = "test",cluster_network = "test")

    def load(self):
        return self


class Osd:
    def __init__(self,*args,**kwargs):
         self.total = 0
         self.used = 0
         self.used_pcnt = 1

    def load(self):
        return self

    def save(self):
        pass


class Pool:
    def __init__(self,*args,**kwargs):
        self.leaves = [maps.NamedDict(key = "test/Pools/test")]
        self._children = [maps.NamedDict(key = "test/Pools/test")]
        self.value = "Pool Name"
        self.pool_name = "test_pool"
        self.used = 100
        self.percent_used = 1

    def load(self):
        return self

    def save(self):
        pass

class Rbd:
    def __init__(self,*args,**kwargs):
        self.name = ""

    def load(self):
        return self
