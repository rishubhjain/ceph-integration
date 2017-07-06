import maps
import __builtin__
import pytest
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.commons import objects
from mock import patch

def test_constructor():
    with patch.object(objects.BaseObject, 'load_definition',return_value = None):
        pool = Pool()
        assert pool is not None
        assert pool.value == 'clusters/{0}/Pools/{1}'
        pool = Pool(pool_id = "1")
        assert pool.pool_id == "1"


def test_render():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.tendrl_context = maps.NamedDict()
    NS.tendrl_context.integration_id = "ceph_integration"
    with patch.object(objects.BaseObject, 'load_definition',return_value = None):
        pool = Pool()
        with patch.object(objects.BaseObject,'_map_vars_to_tendrl_fields',return_value =None):
            ret = pool.render()
            assert ret is not None
