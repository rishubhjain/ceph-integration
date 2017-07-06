import maps
import __builtin__
import pytest
from tendrl.ceph_integration.objects.global_details import GlobalDetails
from tendrl.commons import objects
from mock import patch

def test_constructor():
    with patch.object(objects.BaseObject, 'load_definition',return_value = None):
        global_details = GlobalDetails()
        assert global_details is not None
        assert global_details.value == 'clusters/{0}/GlobalDetails'
        global_details = GlobalDetails(True)
        assert global_details.status is True


def test_render():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.tendrl_context = maps.NamedDict()
    NS.tendrl_context.integration_id = "ceph_integration"
    with patch.object(objects.BaseObject, 'load_definition',return_value = None):
        global_details = GlobalDetails()
        with patch.object(objects.BaseObject,'_map_vars_to_tendrl_fields',return_value =None):
            ret = global_details.render()
