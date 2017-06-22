class TendrlContext():

    def __init__(self, *args):
        self.cluster_id = "test_id"
        self.integration_id = "test_id"
        self.cluster_name = "ceph"

    def load(self,*args):
        return self

    def save(self,*args):
        pass
