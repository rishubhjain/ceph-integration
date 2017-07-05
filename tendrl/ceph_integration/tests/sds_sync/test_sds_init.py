from tendrl.ceph_integration import sds_sync
from tendrl.ceph_integration import ceph
from tendrl.ceph_integration.tests.fixtures.client import Client
from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration.tests.fixtures import cluster
from tendrl.ceph_integration.tests.fixtures import utilization
from tendrl.ceph_integration.tests.fixtures import globaldetails
from tendrl.ceph_integration.tests.fixtures import syncobject
from tendrl.ceph_integration.ceph import AdminSocketNotFoundError
from tendrl.ceph_integration.sds_sync.sync_objects import SyncObjects
from tendrl.ceph_integration.sds_sync import CephIntegrationSdsSyncStateThread
import importlib
import mock
import __builtin__
import maps
import pytest
import socket
from mock import patch
import gevent.event
import etcd
import glob
from tendrl.commons.utils.cmd_utils import Command
from tendrl.ceph_integration.types import SYNC_OBJECT_TYPES
import sys

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
    if args[0] == "no_error":
        out = """out=test\nerror=test\nk=1\nm=1"""
        return maps.NamedDict(err = "",out = out)
    elif args[0] == "get_rbds":
        out = """out=test\nerror test ok\n k = 1"""
        return maps.NamedDict(err = "",out = out,status = 0)
    elif args[0] == "get_rbds_status1":
        out = """out=test\nerror test ok\n k = 1"""
        return maps.NamedDict(err = "",out = out,status = 1)
    elif args[0] == "get_rbds_status with tab":
        out = """out=test\nerror	err = test ok\n k = 1"""
        return maps.NamedDict(err = "",out = out,status = 1)
    elif args[0] == "get_rbds_status:":
        out = """out=test\nerror	err:test ok\n k = 1"""
        return maps.NamedDict(err = "",out = out,status = 1)
    return maps.NamedDict(err = "test error",out = "")


def load_sync(*args):
    raise etcd.EtcdKeyNotFound
    

def rados_command(*args,**kwargs):
    return {'nodes' : [{'kb' : 1, 'kb_used' : 1 ,
                        'utilization' : 1,'id' : 1}]}


def read_pools(*args,**kwargs):
    if args[1] == "clusters/test_id/Pools" or \
        args[1] == "clusters/test_id/Pools/test/pool_name" or \
        args[1] == "clusters/test_id/Pools/test/Rbds" or \
        args[1] == "clusters/test_id/ECProfiles" or \
        args[1] == "clusters/test_id/Osds":
        return utilization.Pool()


def read_raise_error(*args,**kwargs):
    if args[1] == "clusters/test_id/Pools" or \
        args[1] == "clusters/test_id/Pools/test/pool_name" or \
        args[1] == "clusters/test_id/Osds":
        return utilization.Pool()
    elif args[1] == "clusters/test_id/Pools/test/Rbds" or \
        args[1] == "clusters/test_id/ECProfiles":
        raise etcd.EtcdKeyNotFound 


def raise_etcd_error(*args,**kwargs):
    if args[1] == "clusters/test_id/Pools":
        raise etcd.EtcdKeyNotFound
    return utilization.Pool()


def get_rbds(*args,**kwars):
    return {'key':{'size':1,'flags':True,'provisioned':'10','used':'1'}}

@staticmethod
def json_command(*args,**kwargs):
    out = """out
                 RAW USED
                 GLOBAL
                 SIZE AVAIL RAW_USED %RAW_USED
                 10 10 10 10 10"""
    return 1,out,""


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def init():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration."
                                  "tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                    mock.Mock(return_value = maps.NamedDict
                             (fsid = "test_fsid",name='ceph'))):
        return sds_sync.CephIntegrationSdsSyncStateThread()


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
@mock.patch('tendrl.commons.utils.ansible_module_runner.'
            'AnsibleRunner.__init__',mock.Mock(return_value=None))
@mock.patch('tendrl.commons.utils.ansible_module_runner.AnsibleRunner.run',
            mock.Mock(return_value=None))
def test_run():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    setattr(NS, "_int", maps.NamedDict())
    obj = importlib.import_module("tendrl.ceph_integration."
                                  "tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    global sync_obj
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                     mock.Mock(return_value = maps.NamedDict
                              (fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        with patch.object(ceph,'heartbeat',heartbeat) as mock_heartbeat:
            NS.config = maps.NamedDict(
                data = maps.NamedDict(sync_interval = 10))
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
    sync_obj = init()
    cluster_data = {'versions':None}
    ret = sync_obj.on_heartbeat(cluster_data)
    assert ret == None
    cluster_data = {'versions':maps.NamedDict(
                     mds_map = 1.1,osd_map = 1.1,
                     mon_map = 1.1,mon_status = 1.1,
                     pg_summary = 1.1,health = 1.1,config = 1.1)}
    with mock.patch('tendrl.ceph_integration.sds_sync.sync_objects.'
                    'SyncObjects.on_version',mock.Mock(return_value=None)):
        with mock.patch.dict('sys.modules', {'rados': rados}):
            with mock.patch.dict('sys.modules',
                                 {'ceph_argparse': ceph_argparse}):
                with patch.object(Client,'read',read):
                    NS.ceph = maps.NamedDict(objects = utilization)
                    NS.tendrl = maps.NamedDict(objects = cluster)
                    with patch.object(ceph,'ceph_command',ceph_command):
                        with patch.object(Crud,'create',return_value = None):
                            with patch.object(ceph,'rados_command',
                                              return_value = None):
                                sync_obj.on_heartbeat(cluster_data)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_sync_cluster_network_details():
    sync_obj = init()
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
    sync_obj = init()
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
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                    mock.Mock(return_value = maps.NamedDict(
                    fsid = "test_fsid",name='ceph'))):
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
    obj = importlib.import_module("tendrl.ceph_integration."
                                  "tests.fixtures.client")
    NS._int.client = obj.Client()
    NS._int.wclient = obj.Client()
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    with mock.patch('tendrl.ceph_integration.ceph.heartbeat',
                    mock.Mock(return_value = maps.NamedDict
                             (fsid = "test_fsid",name='ceph'))):
        sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
        with mock.patch.dict('sys.modules', {'ceph_argparse': ceph_argparse}):
            with mock.patch.dict('sys.modules', {'rados': rados}):
                NS.ceph = maps.NamedDict(objects = utilization)
                NS._int.client.delete = utilization.Pool
                with patch.object(Client,'read',read_pools):
                    with patch.object(ceph,'rbd_command',ceph_command):
                        sync_obj._sync_rbds()
                    with patch.object(CephIntegrationSdsSyncStateThread,
                                      '_get_rbds',get_rbds):
                        sync_obj._sync_rbds()
                with patch.object(Client,'read',read_raise_error):
                    with patch.object(ceph,'rbd_command',ceph_command):
                        sync_obj._sync_rbds()
                    with patch.object(CephIntegrationSdsSyncStateThread,
                                      '_get_rbds',get_rbds):
                        sync_obj._sync_rbds()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_sync_ec_profiles():
    sync_obj = init()
    with patch.object(ceph,'ceph_command') as mock_ceph_command:
        mock_ceph_command.return_value = ceph_command("no_error")
        with patch.object(Crud,'create',return_value = None):
            with patch.object(Client,'read',read_pools):
                NS._int.client.delete = utilization.Pool
                NS.ceph = maps.NamedDict(objects = utilization)
                sync_obj._sync_ec_profiles()
            with patch.object(Client,'read',read_raise_error):
                NS._int.client.delete = utilization.Pool
                NS.ceph = maps.NamedDict(objects = utilization)
                sync_obj._sync_ec_profiles()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_emit_event():
    sync_obj = init()
    NS.node_context = maps.NamedDict(node_id = None)
    ret = sync_obj._emit_event(1,1,1,"Test_msg")
    assert ret is None
    NS.node_context = maps.NamedDict(node_id = "cpeh_integration")
    NS.publisher_id = "ceph"
    NS.tendrl_context.sds_name = "test_sds"
    sync_obj._emit_event(1,1,1,"Test_msg")
    sync_obj._emit_event(1,1,1,"Test_msg","test_plugin_instance")


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_health():
    sync_obj = init()
    NS.ceph = maps.NamedDict(objects = globaldetails)
    NS.node_context = maps.NamedDict(node_id = "cpeh_integration")
    NS.publisher_id = "ceph"
    NS.tendrl_context.sds_name = "test_sds"
    data = {'overall_status': 'HEALTH_OK'}
    sync_obj._on_health(data)
    data = {'overall_status': 'HEALTH_WARN'}
    sync_obj._on_health(data)
    data = {'overall_status': 'HEALTH_ERR'}
    sync_obj._on_health(data)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_mon_status():
    sync_obj = init()
    NS.ceph = maps.NamedDict(objects = utilization)
    NS.node_context = maps.NamedDict(node_id = "cpeh_integration")
    NS.publisher_id = "ceph"
    NS.tendrl_context.sds_name = "test_sds"
    data = maps.NamedDict(
        quorum = {'mon'},
        mons_by_rank = maps.NamedDict(test_mon = {'name':'test_mon'}))
    sync_obj._on_mon_status(data)
    data = maps.NamedDict(
        quorum = {'test_mon','mon','new_mon'},
        mons_by_rank = maps.NamedDict(new_mon = {'name':'test_mon'}))
    sync_obj._on_mon_status(data)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_osd_map():
    sync_obj = init()
    NS.ceph = maps.NamedDict(objects = utilization)
    NS.node_context = maps.NamedDict(node_id = "cpeh_integration")
    NS.publisher_id = "ceph"
    NS.tendrl_context.sds_name = "test_sds"
    with patch.object(utilization.SyncObject,'exists',return_value = False):
        sync_obj._on_osd_map(data = "")
    data = maps.NamedDict(osds = [{'osd':'temp_osd'}])
    sync_obj._on_osd_map(data)
    data = maps.NamedDict(osds = [{'osd':'test_osd','up':True,'in':True}])
    sync_obj._on_osd_map(data)
    data = maps.NamedDict(osds = [{'osd':'test_osd','up':False,'in':True}])
    sync_obj._on_osd_map(data)
    data = maps.NamedDict(osds = [{'osd':'test_osd','up':True,'in':False}])
    sync_obj._on_osd_map(data)
    data = maps.NamedDict(osds = [{'osd':'test_osd','up':False,'in':False}])
    sync_obj._on_osd_map(data)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_pool_status():
    sync_obj = init()
    NS.ceph = maps.NamedDict(objects = utilization)
    NS.node_context = maps.NamedDict(node_id = "cpeh_integration")
    NS.publisher_id = "ceph"
    NS.tendrl_context.sds_name = "test_sds"
    data = maps.NamedDict(pools = [{'pool':'temp_pool'}])
    sync_obj._on_pool_status(data)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_sync_object():
    sync_obj = init()
    NS.ceph = maps.NamedDict(objects = utilization)
    NS.node_context = maps.NamedDict(node_id = "cpeh_integration")
    NS.publisher_id = "ceph"
    NS.tendrl_context.sds_name = "test_sds"
    sync_obj.fsid = "test_fsid"
    data = {'fsid' : "test_fsid",'type':'health','version':1,'data': {'overall_status':None}}
    sync_obj.on_sync_object(data)
    data = {'fsid' : "test_fsid",'type':'osd_map','version':1,'data': {'overall_status':None,
            'pools':[{'pool':'test_pool','pool_name':'test_name','pg_num':'num',
            'erasure_code_profile':'test','min_size':1,'size':1,
            'quota_max_objects':1,'quota_max_bytes':1}],'osds':
            [{'osd':'test_osd','uuid':'test_uuid','public_addr':'197.1.1.1',
            'cluster_addr':'test_addr','heartbeat_front_addr':'test_addr',
            'heartbeat_back_addr':1,'down_at':'1','up_from':'1',
            'lost_at':2,'up':True,'in':True,'up_thru':'test','weight':1,
            'primary_affinity':'test','state':'test_state',
            'last_clean_begin':1,'last_clean_end':'test'}]}}
    with patch.object(utilization.SyncObject,'exists',return_value = False):
        with patch.object(SyncObjects,'on_fetch_complete',return_value = maps.NamedDict(version = 1.1)):
            with patch.object(Client,'read',read_pools):
                with patch.object(socket,'gethostbyaddr',return_value = "test"):
                    NS._int.client.delete = utilization.Pool
                    sync_obj.on_sync_object(data)
            with patch.object(Client,'read',raise_etcd_error):
                with patch.object(socket,'gethostbyaddr',return_value = "test"):
                    NS._int.client.delete = utilization.Pool
                    sync_obj.on_sync_object(data)
        with patch.object(SyncObjects,'on_fetch_complete',return_value = None):
            sync_obj.on_sync_object(data)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_get_rbds():
    sync_obj = init()
    with patch.object(ceph,'rbd_command') as mock_ceph_command:
        mock_ceph_command.return_value = ceph_command("get_rbds")
        with patch.object(Crud,'create',return_value = None):
            with patch.object(Client,'read',read_pools):
                NS._int.client.delete = utilization.Pool
                NS.ceph = maps.NamedDict(objects = utilization)
                sync_obj._get_rbds("test_pool_name")
        mock_ceph_command.return_value = ceph_command("get_rbds_status1")
        with patch.object(Crud,'create',return_value = None):
            with patch.object(Client,'read',read_pools):
                NS._int.client.delete = utilization.Pool
                NS.ceph = maps.NamedDict(objects = utilization)
                sync_obj._get_rbds("test_pool_name")
        mock_ceph_command.return_value = ceph_command("get_rbds_status:")
        with patch.object(Crud,'create',return_value = None):
            with patch.object(Client,'read',read_pools):
                NS._int.client.delete = utilization.Pool
                NS.ceph = maps.NamedDict(objects = utilization)
                sync_obj._get_rbds("test_pool_name")


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_get_utilization_data():
    sync_obj = init()
    with mock.patch.dict('sys.modules', {'ceph_argparse': ceph_argparse}):
        with mock.patch.dict('sys.modules', {'rados': rados}):
            sync_obj._get_utilization_data()
            with patch.object(ceph_argparse,'json_command',json_command):
                with pytest.raises(Exception):
                    sync_obj._get_utilization_data()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_idx_in_list():
    sync_obj = init()
    ret = sync_obj._idx_in_list([],"test")
    assert ret == -1


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_to_bytes():
    sync_obj = init()
    ret = sync_obj._to_bytes("1K")
    assert ret == 1024
    ret = sync_obj._to_bytes("1M")
    assert ret == 1048576
    ret = sync_obj._to_bytes("1G")
    assert ret == 1073741824
    ret = sync_obj._to_bytes("1T")
    assert ret == 1099511627776
    ret = sync_obj._to_bytes("1P")
    assert ret == 1125899906842624


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_get_sync_object_data():
    sync_obj = init()
    cls = importlib.import_module('tendrl.ceph_integration.types').MdsMap
    ret = sync_obj.get_sync_object_data(cls)
    assert ret is None


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_get_sync_object():
    sync_obj = init()
    cls = importlib.import_module('tendrl.ceph_integration.types').MdsMap
    ret = sync_obj.get_sync_object(cls)
    assert isinstance(ret,cls)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_request_delete():
    sync_obj = init()
    with pytest.raises(NotImplementedError):
        sync_obj.request_delete("crush_map",1)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_request_create():
    sync_obj = init()
    with pytest.raises(NotImplementedError):
        sync_obj.request_create("crush_map",1)
