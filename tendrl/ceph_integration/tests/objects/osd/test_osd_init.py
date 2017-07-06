import pytest
from tendrl.commons import objects
from mock import patch

def test_constructor():
    with patch.object(objects.BaseObject, 'load_definition',return_value = None):
        #osd = Osd()
        pass
