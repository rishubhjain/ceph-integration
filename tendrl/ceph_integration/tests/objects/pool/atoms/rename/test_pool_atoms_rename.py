import __builtin__
import importlib
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.pool.atoms.rename import Rename
from tendrl.commons import objects
from tendrl.ceph_integration.tests.fixtures.client import Client
from tendrl.ceph_integration.manager.crud import Crud

'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        rename = Rename()
        assert rename is not None


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
        rename = Rename(parameters = {'Pool.pool_id' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','Pool.poolname':'test'})
        with patch.object(Crud,'update',return_value = {'request': maps.NamedDict(state = "",error = "",id = 1)}):
            with patch.object(Client,'read',return_value = maps.NamedDict(value = "")):
                ret = rename.run()
                assert ret is False
                with patch.object(Crud,'sync_request_status',return_value = None):
                    ret = rename.run()
                    assert ret is True
