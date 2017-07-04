from tendrl.ceph_integration import sds_sync
from tendrl.ceph_integration import ceph
from tendrl.ceph_integration.tests.fixtures.client import Client
from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration.tests.fixtures import cluster
from tendrl.ceph_integration.tests.fixtures import utilization
from tendrl.ceph_integration.tests.fixtures import syncobject
from tendrl.ceph_integration.ceph import AdminSocketNotFoundError
import importlib
import mock
import __builtin__
import maps
import pytest
from mock import patch
import gevent.event
import etcd
import glob
from tendrl.commons.utils.cmd_utils import Command
from tendrl.ceph_integration.types import SYNC_OBJECT_TYPES


'''Global Variables'''


sync_obj = None


'''Dummy functions'''

class ceph_argparse:

    def __init__(self):
        pass

    @staticmethod
    def json_command(*args,**kwargs):
        out = """out
                 RAW USED
                 GLOBAL
                 SIZE AVAIL RAW_USED %RAW_USED
                 10 10 10 10 10"""
        return 0,out,""
    

class rados:
    Error = ""
    def __init__(self):
        pass

    @staticmethod
    def Rados(*args,**kwargs):
        return rados()

    def connect(self):
        pass

    def shutdown(self):
        pass

    @staticmethod
    def Error(*args):
        raise Exception


def get_heartbeats(*args,**kwargs):
    return 1.1,[{
        'cluster': "test_cluster_name",
        'type': "mon",
        'id': 1,
        'fsid': "test_fsid",
        'status': maps.NamedDict(rank = 1,quorum = True),
        'ceph_version': service_version
    }]

def ping_cluster(*args):
    args[0].name = "ceph"

def heartbeat(*args,**kwargs):
    sync_obj._complete.set()
    return None

def read(*args,**kwargs):
    raise etcd.EtcdKeyNotFound


def write(*args):
    raise etcd.EtcdAlreadyExist


def run(*args):
    if args[0]:
        out = """out
                 error = test"""
        return out,"err",0
    else:
        return "out","err",1


def run_None(*args):
    return None,"err",0


def ceph_command(*args):
    return maps.NamedDict(err = "test error",out = "")


def load_sync(*args):
    raise etcd.EtcdKeyNotFound
    

def rados_command(*args,**kwargs):
    return {'nodes' : [{'kb' : 1, 'kb_used' : 1 ,
                        'utilization' : 1,'id' : 1}]}


def read_pools(*args,**kwargs):
    if args[1] == "clusters/test_id/Pools" or \
        args[1] == "clusters/test_id/Pools/test/pool_name" or \
        args[1] == "clusters/test_id/Pools/test/Rbds":
        return utilization.Pool()


'''Unit Test Cases'''


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_contructor():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                     mock.Mock(return_value = maps.NamedDict
                              (fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        assert sync_obj is not None
    with patch.object(sds_sync.CephIntegrationSdsSyncStateThread,
                      '_ping_cluster',ping_cluster):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        assert sync_obj is not None
        assert isinstance(sync_obj._request_factories,dict)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_ping_cluster():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with pytest.raises(AdminSocketNotFoundError):
        with mock.patch.dict('sys.modules', {'rados': rados}):
            sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
            sync_obj._ping_cluster()
            assert sync_obj.name is None
    NS.tendrl_context.cluster_id = None
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                    mock.Mock(return_value = maps.NamedDict
                             (fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        sync_obj._ping_cluster()
        assert sync_obj.name is "ceph"
    NS.tendrl_context.cluster_id = None
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                     mock.Mock(return_value = maps.NamedDict(name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        sync_obj._ping_cluster()
        assert sync_obj.name is "ceph"
    NS.tendrl_context.cluster_id = None
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                     mock.Mock(return_value = None)):
        with pytest.raises(TypeError):
            sync_obj._ping_cluster()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
@mock.patch('gevent.sleep',
            mock.Mock(return_value=True))
@mock.patch('tendrl.commons.utils.ansible_module_runner.AnsibleRunner.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.utils.ansible_module_runner.AnsibleRunner.run',
            mock.Mock(return_value=None))
def test_run():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    global sync_obj
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                     mock.Mock(return_value = maps.NamedDict
                              (fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        with patch.object(ceph,'heartbeat',heartbeat) as mock_heartbeat:
            NS.config = maps.NamedDict(data = maps.NamedDict(sync_interval = 10))
            NS.tendrl = maps.NamedDict(objects = cluster)
            sync_obj._run()
            with patch.object(cluster.Cluster,'exists',return_value = False):
                sync_obj._run()
            with patch.object(Client,'write',write):
                sync_obj._run()
            with patch.object(Client,'read',read):
                with patch.object(Command,'run') as mock_run:
                    mock_run.return_value = run(True)
                    sync_obj._run()
                    mock_run.return_value = run(False)
                    sync_obj._run()
                with patch.object(Command,'run',run_None) as mock_run:
                    sync_obj._run()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_heartbeat():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                    mock.Mock(return_value = maps.NamedDict
                             (fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        cluster_data = {'versions':None}
        ret = sync_obj.on_heartbeat(cluster_data)
        assert ret == None
        cluster_data = {'versions':maps.NamedDict(mds_map = 1.1,osd_map = 1.1,mon_map = 1.1,mon_status = 1.1,pg_summary = 1.1,health = 1.1,config = 1.1)}
        with mock.patch('tendrl.ceph_integration.sds_sync.sync_objects.SyncObjects.on_version',mock.Mock(return_value=None)):
            with mock.patch.dict('sys.modules', {'rados': rados}):
                with mock.patch.dict('sys.modules', {'ceph_argparse': ceph_argparse}):
                    with patch.object(Client,'read',read):
                        NS.ceph = maps.NamedDict(objects = utilization)
                        NS.tendrl = maps.NamedDict(objects = cluster)
                        with patch.object(ceph,'ceph_command',ceph_command):
                            with patch.object(Crud,'create',return_value = None):
                                with patch.object(ceph,'rados_command',return_value = None):
                                    sync_obj.on_heartbeat(cluster_data)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_sync_cluster_network_details():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',mock.Mock(return_value = maps.NamedDict(fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        with patch.object(Client,'read',read):
            NS.ceph = maps.NamedDict(objects = utilization)
            with patch.object(utilization.SyncObject,'load',load_sync):
                with pytest.raises(etcd.EtcdKeyNotFound):
                    sync_obj._sync_cluster_network_details()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_sync_osd_utilization():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',mock.Mock(return_value = maps.NamedDict(fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        with mock.patch.dict('sys.modules', {'rados': rados}):
            with mock.patch.dict('sys.modules', {'ceph_argparse': ceph_argparse}):
                with patch.object(ceph,'rados_command',rados_command):
                    NS.ceph = maps.NamedDict(objects = utilization)
                    sync_obj._sync_osd_utilization()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_sync_utilization():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',mock.Mock(return_value = maps.NamedDict(fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        with mock.patch.dict('sys.modules', {'ceph_argparse': ceph_argparse}):
            with mock.patch.dict('sys.modules', {'rados': rados}):
                NS.ceph = maps.NamedDict(objects = utilization)
                with patch.object(Client,'read',read_pools):
                    sync_obj._sync_utilization()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_sync_rbds():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',mock.Mock(return_value = maps.NamedDict(fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        with mock.patch.dict('sys.modules', {'ceph_argparse': ceph_argparse}):
            with mock.patch.dict('sys.modules', {'rados': rados}):
                NS.ceph = maps.NamedDict(objects = utilization)
                NS._int.client.delete = utilization.Pool
                with patch.object(Client,'read',read_pools):
                    with patch.object(ceph,'rbd_command',ceph_command):
                        sync_obj._sync_rbds()
