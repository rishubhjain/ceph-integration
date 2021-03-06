import json
import uuid

import etcd

job_id1 = str(uuid.uuid4())

job = {
    "integration_id": "ab3b125e-4769-4071-a349-e82b380c11f4",
    "run": "tendrl.ceph_integration.flows.CreatePool",
    "status": "new",
    "parameters": {
        "Pool.poolname": 'test',
        "Pool.pg_num": 1,
        "Pool.min_size": 1
    },
    "type": "node",
    "node_ids": ["635ead0b-6ba3-47c9-a054-009e65acea3e"]
}

print("/queue/%s/" % job_id1)
client = etcd.Client(host="localhost", port=2379)
client.write("/queue/%s" % job_id1, None, dir=True)
client.write("/queue/%s/payload" % job_id1, json.dumps(job))
client.write("/queue/%s/status" % job_id1, "new")
