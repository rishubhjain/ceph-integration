import __builtin__
import importlib
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.ecprofile.atoms.delete import Delete
from tendrl.ceph_integration.manager.exceptions import \
    RequestStateError
from tendrl.commons import objects
from tendrl.ceph_integration.manager.crud import Crud

'''Dummy Function'''


def sync_request_status(*args):
    raise RequestStateError

'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        ec_profile = Delete()
        assert isinstance(ec_profile.parameters,dict)



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
    ecprofile = importlib.import_module("tendrl.ceph_integration.tests.fixtures.ecprofile")
    clt = importlib.import_module("tendrl.ceph_integration.tests.fixtures.client").Client()
    NS._int = maps.NamedDict(wclient = clt)
    NS.ceph = maps.NamedDict(objects = ecprofile)
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        ec_profile = Delete(parameters = {'ECProfile.name' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','ECProfile.plugin' : 'test_plugin','ECProfile.k' : 'k','ECProfile.m' : 'm'})
        with patch.object(Crud,'delete',return_value = {'request':'test'}):
            with patch.object(Crud,'sync_request_status',return_value = None):
                ret = ec_profile.run()
                assert ret is True
        ec_profile = Delete(parameters = {'ECProfile.name' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id','ECProfile.directory' : 'directory','ECProfile.k' : 'k','ECProfile.m' : 'm'})
        with patch.object(Crud,'delete',return_value = {'request':'test'}):
            with patch.object(Crud,'sync_request_status',return_value = None):
                ret = ec_profile.run()
                assert ret is True
        with patch.object(Crud,'delete',return_value = {'request':'test'}):
            with patch.object(Crud,'sync_request_status',sync_request_status):
                ret = ec_profile.run()
                assert ret is False
