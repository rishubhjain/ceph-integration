import __builtin__
import etcd
import importlib
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.ecprofile.atoms.check_ec_profile_available import  CheckECProfileAvailable
from tendrl.commons import objects
from tendrl.ceph_integration.tests.fixtures.ecprofile import ECProfile
from tendrl.commons.objects import AtomExecutionFailedError

'''Dummy Functions'''

def load(*args):
    raise etcd.EtcdKeyNotFound


'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        ec_profile = CheckECProfileAvailable()
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
    NS.ceph = maps.NamedDict(objects = ecprofile)
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        ec_profile = CheckECProfileAvailable(parameters = {'ECProfile.name' : 'test_param','job_id':'test_job_id','flow_id':'test_flow_id'})
        ec_profile.run()
        with patch.object(ECProfile,'load',load):
            with pytest.raises(AtomExecutionFailedError):
                ec_profile.run()
    
