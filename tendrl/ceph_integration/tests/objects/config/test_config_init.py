import pytest
from tendrl.commons import config as cmn_config
from tendrl.ceph_integration.objects.config import Config

def test_config_init():
    config = Config()
