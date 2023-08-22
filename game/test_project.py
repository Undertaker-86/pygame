import pytest
from project import *

def test_toggle_music():
    assert toggle_music(True) == False
    assert toggle_music(False) == True



