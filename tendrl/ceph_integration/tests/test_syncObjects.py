from tendrl.ceph_integration.sds_sync.sync_objects import SyncObjects


class Test_SyncObjects(object):

    def test_SyncObjects(self):
        self.sync_object = SyncObjects("test_cluster")
