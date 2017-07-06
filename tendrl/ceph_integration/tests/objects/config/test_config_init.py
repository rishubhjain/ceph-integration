import pytest
from mock import patch
from tendrl.commons import config as cmn_config
from tendrl.ceph_integration.objects.config import Config


def test_config_init():
    with patch.object(cmn_config,'load_config',return_value = True):
        config = Config()
        assert config.value == "_NS/ceph/config"
        config = Config("test_config")
        assert config.data == "test_config"
