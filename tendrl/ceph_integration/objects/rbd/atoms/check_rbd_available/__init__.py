import etcd
import gevent

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError


class CheckRbdAvailable(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(CheckRbdAvailable, self).__init__(*args, **kwargs)

    def run(self):
        retry_count = 0
        while True:
            try:
                NS.ceph.objects.Rbd(
                    pool_id=self.parameters['Rbd.pool_id'],
                    name=self.parameters['Rbd.name']
                ).load()
                return True
            except etcd.EtcdKeyNotFound:
                retry_count += 1
                gevent.sleep(1)
                if retry_count == 600:
                    Event(
                        Message(
                            priority="error",
                            publisher=NS.publisher_id,
                            payload={
                                "message": "Rbd %s not reflected in "
                                "tendrl yet. Timing out" %
                                self.parameters['Rbd.name']
                            },
                            job_id=self.parameters['job_id'],
                            flow_id=self.parameters['flow_id'],
                            cluster_id=NS.tendrl_context.integration_id,
                        )
                    )
                    raise AtomExecutionFailedError(
                        "Rbd %s not reflected in tendrl yet. Timing out" %
                        self.parameters['Rbd.name']
                    )
