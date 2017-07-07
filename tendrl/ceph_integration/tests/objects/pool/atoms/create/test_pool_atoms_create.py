import __builtin__
import importlib
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.pool.atoms.create import Create
from tendrl.commons import objects
from tendrl.ceph_integration.manager.crud import Crud

'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        create = Create()



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
        create = Create(parameters = {'Pool.pg_num' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','Pool.min_size':'1','Pool.poolname':'test','Pool.size':1,'Pool.type':str,'Pool.erasure_code_profile':'test_code'})
        with patch.object(Crud,'create',return_value = {'request': maps.NamedDict(state = "",error = "",id = 1)}):
            ret = create.run()
            assert ret is False
            with patch.object(Crud,'sync_request_status',return_value = None):
                ret = create.run()
                assert ret is True
                create.parameters['Pool.type'] = "erasure"
                ret = create.run()
                assert ret is True
                create.parameters['Pool.quota_enabled'] = True
                ret = create.run()
                assert ret is True
