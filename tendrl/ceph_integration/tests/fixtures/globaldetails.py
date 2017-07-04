class GlobalDetails:

    def __init__(self,*args,**kwargs):
       self.status = "HEALTH_WARN"

    def save(self):
        pass

    def load(self):
        return self
