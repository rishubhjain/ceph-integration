from tendrl.ceph_integration.sds_sync.sync_objects import SyncObjects
from tendrl.ceph_integration import ceph
import pytest
from mock import patch
import importlib
import mock
import __builtin__
import maps
import datetime
from pytz import utc


def test_SyncObjects():
    sync_object = SyncObjects("test_cluster")
    assert isinstance(sync_object._objects,dict)
    assert sync_object._cluster_name == "test_cluster"


def test_set_map():
    sync_object = SyncObjects("test_cluster")
    typ = importlib.import_module("tendrl.ceph_integration.types").Health
    ret = sync_object.set_map(typ,1.0,"test")
    assert ret is not None
    assert isinstance(ret,typ)

def test_get_version():
    sync_object = SyncObjects("test_cluster")
    typ = importlib.import_module("tendrl.ceph_integration.types").Health
    sync_object._objects[typ].version = 1.1
    ret = sync_object.get_version(typ)
    assert ret == 1.1
    typ = importlib.import_module("tendrl.ceph_integration.tests.fixtures.sds").Sds
    sync_object._objects[typ] = None
    ret = sync_object.get_version(typ)
    assert ret is None

def test_get_data():
    sync_object = SyncObjects("test_cluster")
    typ = importlib.import_module("tendrl.ceph_integration.types").Health
    sync_object._objects[typ].data = "test_data"
    ret = sync_object.get_data(typ)
    assert ret == "test_data"
    typ = importlib.import_module("tendrl.ceph_integration.tests.fixtures.sds").Sds
    sync_object._objects[typ] = None
    ret = sync_object.get_data(typ)
    assert ret is None

def test_get():
    sync_object = SyncObjects("test_cluster")
    typ = importlib.import_module("tendrl.ceph_integration.types").Health
    ret = sync_object.get(typ)
    assert isinstance(ret,typ)

@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_version():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    sync_object = SyncObjects("test_cluster")
    typ = importlib.import_module("tendrl.ceph_integration.types").Health
    sync_object._objects[typ].version = 1.1
    with patch.object(ceph,'get_cluster_object',return_value = None):
        ret = sync_object.on_version(typ,2.2)
    with patch.object(ceph,'get_cluster_object',return_value = None):
        ret = sync_object.on_version(typ,0.1)
    sync_object._fetching_at[typ] = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1)
    with patch.object(ceph,'get_cluster_object',return_value = None):
        ret = sync_object.on_version(typ,2.2)


@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_on_fetch_complete():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.publisher_id = "ceph_integration"
    sync_object = SyncObjects("test_cluster")
    typ = importlib.import_module("tendrl.ceph_integration.types").Health
    ret = sync_object.on_fetch_complete(typ,1.1,"test_data")
    assert isinstance(ret,typ)
    sync_object._objects[typ].version = 1.1
    ret = sync_object.on_fetch_complete(typ,1.1,"test_data")
    assert ret is None
