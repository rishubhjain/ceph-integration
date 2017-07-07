import __builtin__
import importlib
import maps
import mock
from mock import patch
import pytest
import importlib
from tendrl.ceph_integration.objects.pool.atoms.delete import Delete
from tendrl.commons import objects
from tendrl.ceph_integration.manager.crud import Crud

'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        delete = Delete()



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
    clt = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client").Client()
    NS._int = maps.NamedDict(wclient = clt)
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        delete = Delete(parameters = {'ECProfile.name' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','Pool.min_size':'1','Pool.poolname':'test','Pool.size':1,'Pool.type':str,'Pool.erasure_code_profile':'test_code','Pool.pool_id':1})
        with patch.object(Crud,'delete',return_value = {'request': maps.NamedDict(state = "",error = "",id = 1)}):
            ret = delete.run()
            assert ret is False
            with patch.object(Crud,'sync_request_status',return_value = None):
                ret = delete.run()
                assert ret is True
                delete.parameters['Pool.type'] = "erasure"
                ret = delete.run()
                assert ret is True
                delete.parameters['Pool.quota_enabled'] = True
                ret = delete.run()
                assert ret is True
