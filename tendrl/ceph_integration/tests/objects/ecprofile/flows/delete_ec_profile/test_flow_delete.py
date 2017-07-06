import __builtin__
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.ecprofile.flows.delete_ec_profile import DeleteECProfile
from tendrl.commons import flows


'''Unit Test Cases'''


def test_constructor():
    with patch.object(flows.BaseFlow, 'load_definition',return_value = {'uuid' :"Test_uuid",'help': "test_help"}) as mock_load:
        ec_profile = DeleteECProfile()
        assert mock_load.called



@mock.patch('tendrl.commons.event.Event.__init__',
            mock.Mock(return_value=None))
@mock.patch('tendrl.commons.message.Message.__init__',
            mock.Mock(return_value=None))
def test_run():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.tendrl_context = maps.NamedDict()
    NS.tendrl_context.integration_id = "ceph_integration"
    NS.publisher_id = "ceph_integration"
    with patch.object(flows.BaseFlow, 'load_definition',return_value = {'uuid' :"Test_uuid",'help': "test_help"}) as mock_load:
        ec_profile = DeleteECProfile(parameters = {'ECProfile.name' : 'test_param'})
        ec_profile.to_str = "test"
        ec_profile.run()
