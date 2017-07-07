import __builtin__
import etcd
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.pool.atoms.pool_exists import PoolExists
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.commons import objects


'''Dummy Functions'''

def load(*args,**kwargs):
    raise etcd.EtcdKeyNotFound


'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        named_pool = PoolExists()


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
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        named_pool = PoolExists(parameters = {'Pool.pool_id' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','Pool.min_size':'1','Pool.poolname':'test_pool'})
        with patch.object(objects.BaseObject, 'load_definition',return_value = None):
            with patch.object(objects.BaseObject,'_map_vars_to_tendrl_fields',return_value =None):
                with patch.object(Pool,'load',return_value = None):
                    ret = named_pool.run()
                    assert ret is True
                with patch.object(Pool,'load',load):
                    ret = named_pool.run()
                    assert ret is False
