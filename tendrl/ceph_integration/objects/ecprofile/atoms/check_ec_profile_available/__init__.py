import etcd
import gevent

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError


class CheckECProfileAvailable(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(CheckECProfileAvailable, self).__init__(*args, **kwargs)

    def run(self):
        retry_count = 0
        while True:
            try:
                NS.ceph.objects.ECProfile(
                    name=self.parameters['ECProfile.name']
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
                                "message": "ECProfile %s not reflected"\
                                " in tendrl yet. Timing out" %
                                self.parameters['ECProfile.name']
                            },
                            job_id=self.parameters['job_id'],
                            flow_id=self.parameters['flow_id'],
                            cluster_id=NS.tendrl_context.integration_id,
                       )
                    )
                    raise AtomExecutionFailedError(
                        "ECProfile %s not reflected in tendrl yet. Timing out" %
                        self.parameters['ECProfile.name']
                    )
