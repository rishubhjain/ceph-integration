import __builtin__
import etcd
import importlib
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.pool.atoms.check_pool_available import CheckPoolAvailable
from tendrl.commons import objects
from tendrl.ceph_integration.tests.fixtures.client import Client
from tendrl.commons.objects import AtomExecutionFailedError

'''Dummy Functions'''

def raise_etcd(*args):
    raise etcd.EtcdKeyNotFound

def read(*args):
    if args[0] == "test_read":
        return None

def read_pool(*args):
    return maps.NamedDict(leaves = [maps.NamedDict(key = "test/Pools/test_pool")],value = "")


def load(*args):
    raise etcd.EtcdKeyNotFound

'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        check_pool = CheckPoolAvailable()
        assert isinstance(check_pool.parameters,dict)



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
        check_pool = CheckPoolAvailable(parameters = {'name' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','Pool.pool_name':'test','Pool.poolname':'test'})
        with pytest.raises(AtomExecutionFailedError):
            check_pool.run()
        with patch.object(Client,'read',raise_etcd):
            with pytest.raises(AtomExecutionFailedError):
                check_pool.run()
        with patch.object(Client,'read',read) as mock_read:
            mock_read.return_value = read("test_read")
            with pytest.raises(AtomExecutionFailedError):
                check_pool.run()
        with patch.object(Client,'read',return_value = maps.NamedDict(leaves = [])) as mock_read:
            with pytest.raises(AtomExecutionFailedError):
                check_pool.run()
        with patch.object(objects.BaseObject, 'load_definition',return_value = None):
            with patch.object(objects.BaseObject,'_map_vars_to_tendrl_fields',return_value =None):
                with patch.object(Client,'read',read_pool) as mock_read:
                    with patch.object(objects.BaseObject,'load',return_value = maps.NamedDict(pool_name = 'test')):
                        ret = check_pool.run()
                        assert ret is True
                    with patch.object(objects.BaseObject,'load',load):
                        with pytest.raises(AtomExecutionFailedError):
                            ret = check_pool.run()
                            assert ret is True
                            check_pool = CheckPoolAvailable(parameters = {'name' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','Pool.pool_name':'test','Pool.poolname':'_pool'})                       
                            with pytest.raises(AtomExecutionFailedError):
                                ret = check_pool.run()
