import maps
import __builtin__
import pytest
from tendrl.ceph_integration.objects.ecprofile import ECProfile
from tendrl.commons import objects
from mock import patch

def test_constructor():
    with patch.object(objects.BaseObject, 'load_definition',return_value = None):
        ec_profile = ECProfile()
        assert ec_profile is not None
        assert ec_profile.value == 'clusters/{0}/ECProfiles/{1}'
        ec_profile = ECProfile(name = "test_name")
        assert ec_profile.name == "test_name"


def test_render():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.tendrl_context = maps.NamedDict()
    NS.tendrl_context.integration_id = "ceph_integration"
    with patch.object(objects.BaseObject, 'load_definition',return_value = None):
        ec_profile = ECProfile()
        with patch.object(objects.BaseObject,'_map_vars_to_tendrl_fields',return_value =None):
            ret = ec_profile.render()
