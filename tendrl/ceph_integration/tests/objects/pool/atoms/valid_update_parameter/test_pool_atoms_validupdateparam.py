import __builtin__
import importlib
import maps
import mock
from mock import patch
import pytest
from tendrl.ceph_integration.objects.pool.atoms.valid_update_parameters import ValidUpdateParameters
from tendrl.commons import objects
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.ceph_integration.manager.crud import Crud
from tendrl.commons.objects import AtomExecutionFailedError

'''Unit Test Cases'''


def test_constructor():
    with patch.object(objects.BaseAtom, 'load_definition',return_value = None):
        update = ValidUpdateParameters()


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
        update = ValidUpdateParameters(parameters = {
            'Pool.pg_num' :1,'job_id':'test_job_id','flow_id':'test_flow_id',
            'Pool.pool_id':1})
        with patch.object(objects.BaseObject, 'load_definition',return_value = None):
            with patch.object(objects.BaseObject,'_map_vars_to_tendrl_fields',return_value =None):
                with patch.object(Pool,'load',return_value = maps.NamedDict(
                    pg_num = 1)):
                    with pytest.raises(AtomExecutionFailedError):
                            ret = update.run()
                    with patch.object(Pool,'load',return_value = maps.NamedDict(
                        pg_num = 0)):
                        ret = update.run()
                        update.parameters.pop('Pool.pg_num')
                        ret = update.run()
                        assert ret is True
