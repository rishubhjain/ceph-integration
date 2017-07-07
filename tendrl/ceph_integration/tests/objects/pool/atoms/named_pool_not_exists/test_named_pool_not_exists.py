import __builtin__
import etcd
import importlib
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.pool.atoms.named_pool_not_exists import NamedPoolNotExists
from tendrl.ceph_integration.tests.fixtures.client import Client
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.ceph_integration.tests.fixtures.utilization import Pool as pool_dummy
from tendrl.commons import objects
'''Dummy Functions'''

def read(*args,**kwargs):
    raise etcd.EtcdKeyNotFound
'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        named_pool = NamedPoolNotExists()



@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
@mock.patch('gevent.sleep',
            mock.Mock(return_value=True))
def test_run():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.tendrl_context = maps.NamedDict()
    NS.tendrl_context.integration_id = "ceph_integration"
    NS.publisher_id = "ceph_integration"
    client = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client").Client()
    NS._int = maps.NamedDict(client = client)
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        named_pool = NamedPoolNotExists(parameters = {'Pool.pg_num' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','Pool.min_size':'1','Pool.poolname':'test_pool','Pool.size':1,'Pool.type':str,'Pool.erasure_code_profile':'test_code'})
        with patch.object(objects.BaseObject, 'load_definition',return_value = None):
            with patch.object(objects.BaseObject,'_map_vars_to_tendrl_fields',return_value =None):
                with patch.object(Client,'read',return_value = pool_dummy()):
                    ret = named_pool.run()
                    assert ret is True
                    with patch.object(Pool,'load',return_value = maps.NamedDict(pool_name = "test_pool")):
                        ret = named_pool.run()
                        assert ret is False
                with patch.object(Client,'read',read):
                    ret = named_pool.run()
                    assert ret is True
