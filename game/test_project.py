import pytest
from project import *

def test_get_current_time():
    global start_time
    start_time = 0
    # Games will terminate immediately, so current_time should be zero
    assert get_current_time() == 0

def test_display_score():
    global start_time
    start_time = 0
    assert display_score() == 0

def test_collision_sprite():
    #Default state should return True
    assert collision_sprite() == True

def test_toggle_music():
    assert toggle_music(True) == False
    assert toggle_music(False) == True



