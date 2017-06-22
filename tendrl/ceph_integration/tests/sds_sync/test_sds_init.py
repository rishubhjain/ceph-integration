from tendrl.ceph_integration import sds_sync
from tendrl.ceph_integration import ceph
from tendrl.ceph_integration.tests.fixtures.client import Client
import importlib
import mock
import __builtin__
import maps
from mock import patch
import gevent.event
import etcd
from tendrl.commons.utils.cmd_utils import Command

'''Global Variables'''

sync_obj = None

'''Dummy functions'''

def ping_cluster(*args):
    args[0].name = "ceph"

def heartbeat(*args,**kwargs):
    sync_obj._complete.set()
    return None

def read(*args):
    raise etcd.EtcdKeyNotFound

def run(*args):
    if args[0]:
        out = out = """out
                       error = test"""

        return out,"err",0
    else:
        return "out","err",1
    
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
    sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
    assert sync_obj is not None
    with patch.object(sds_sync.CephIntegrationSdsSyncStateThread,'_ping_cluster',ping_cluster):
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
    sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
    sync_obj._ping_cluster()
    assert sync_obj.name is "None"
    NS.tendrl_context.cluster_id = None
    sync_obj._ping_cluster()
    with patch.object(ceph,'heartbeat',return_value = {'fsid': 'test_fsid','name':'ceph'}):
        sync_obj._ping_cluster()
        assert sync_obj.name is "ceph"


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
    sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
    with patch.object(ceph,'heartbeat',heartbeat) as mock_heartbeat:
        sync_obj._run()
        #assert mock_heartbeat.assert_called()
        with patch.object(Client,'read',read):
            with patch.object(Command,'run') as mock_run:
                mock_run.return_value = run(True)
                sync_obj._run()
                mock_run.return_value = run(False)
                sync_obj._run()


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_heartbeat():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    NS.tendrl_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.tendrlcontext").TendrlContext()
    NS.node_context = importlib.import_module("tendrl.ceph_integration.tests.fixtures.nodecontext").NodeContext()
    sync_obj = sds_sync.CephIntegrationSdsSyncStateThread()
    cluster_data = {'versions':None}
    ret = sync_obj.on_heartbeat(cluster_data)
    assert ret == None
