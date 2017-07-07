import etcd
import gevent

from tendrl.ceph_integration.objects.pool import Pool
from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError


class CheckPoolAvailable(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(CheckPoolAvailable, self).__init__(*args, **kwargs)

    def run(self):
        retry_count = 0
        while True:
            pools = None
            try:
                pools = NS._int.client.read(
                    "clusters/%s/Pools" % NS.tendrl_context.integration_id
                )
            except etcd.EtcdKeyNotFound:
                pass
            
            if pools:
                for entry in pools.leaves:
                    try:
                        pool = Pool(pool_id=entry.key.split("Pools/")[-1]).load()
                        if pool.pool_name == self.parameters['Pool.poolname']:
                            return True
                    except etcd.EtcdKeyNotFound:
                        continue
            
            retry_count += 1
            gevent.sleep(1)
            if retry_count == 600:
                Event(
                    Message(
                        priority="error",
                        publisher=NS.publisher_id,
                        payload={
                            "message": "Pool %s not reflected in tendrl yet. Timing out" %
                            self.parameters['Pool.poolname']
                        },
                        job_id=self.parameters['job_id'],
                        flow_id=self.parameters['flow_id'],
                        cluster_id=NS.tendrl_context.integration_id,
                   )
                )
                raise AtomExecutionFailedError(
                    "Pool %s not reflected in tendrl yet. Timing out" %
                    self.parameters['Pool.poolname']
                )
