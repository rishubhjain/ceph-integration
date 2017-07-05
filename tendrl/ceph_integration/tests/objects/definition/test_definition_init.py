import maps
import __builtin__
import pytest
from tendrl.ceph_integration.objects.definition import Definition
import sys


def test_constructor():
    def_con = Definition()
    assert def_con is not None
    assert def_con.value == 'clusters/{0}/_NS/definitions'


def test_get_parsed_defs():
    def_con = Definition()
    ret = def_con.get_parsed_defs()
    assert ret is not None
    def_con._parsed_defs = None
    ret_test = def_con.get_parsed_defs()
    assert ret == ret_test


def test_render():
    setattr(__builtin__, "NS", maps.NamedDict())
    NS.tendrl_context = maps.NamedDict()
    NS.tendrl_context.integration_id = "ceph_integration"
    def_con = Definition()
    ret = def_con.render()
    assert def_con.value == 'clusters/ceph_integration/_NS/definitions'
