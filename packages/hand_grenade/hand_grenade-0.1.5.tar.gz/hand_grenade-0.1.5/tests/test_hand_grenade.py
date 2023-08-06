from math import inf

import pytest

from hand_grenade import HandGrenade


def test_bounds():
    with pytest.raises(KeyError):
        HandGrenade({0: 'zero'}, lower=1)
    with pytest.raises(KeyError):
        assert not HandGrenade()[0]
    grenade = HandGrenade({0: 'zero'})
    assert grenade[-inf] == 'zero'
    assert grenade[inf] == 'zero'
    grenade = HandGrenade({0: 'zero'}, lower=-10, upper=10)
    assert grenade[-10] == 'zero'
    assert grenade[10] == 'zero'
    with pytest.raises(KeyError):
        assert not grenade[-11]
    with pytest.raises(KeyError):
        assert not grenade[11]
    grenade = HandGrenade({2: 'two', 9: 'nine'}, lower=1, upper=10)
    assert grenade[1] == 'two'
    assert grenade[10] == 'nine'
    with pytest.raises(KeyError):
        assert not grenade[0]
    with pytest.raises(KeyError):
        assert not grenade[11]


def test_clear():
    grenade = HandGrenade({0: 'zero'})
    assert grenade[0] == 'zero'
    grenade.clear()
    with pytest.raises(KeyError):
        assert not grenade[0]


def test_construction():
    assert not HandGrenade()
    grenade = HandGrenade({0: 'zero'})
    assert len(grenade) == 1
    grenade = HandGrenade({0: 'zero', 4: 'four'})
    assert len(grenade) == 2


def test_contains():
    assert 0 not in HandGrenade()
    grenade = HandGrenade({0: 'zero'})
    for i in [-inf, -10, 0, 20, inf]:
        assert i in grenade


def test_copy():
    grenade = HandGrenade({0: 'zero'})
    assert grenade == grenade.copy()
    assert grenade is not grenade.copy()


def test_equality():
    assert HandGrenade() == HandGrenade()
    dictionary = {0: 'zero'}
    grenade = HandGrenade(dictionary)
    assert dictionary != grenade
    assert grenade == HandGrenade(dictionary)
    assert grenade != HandGrenade(dictionary, lower=0)
    assert grenade != HandGrenade(dictionary, upper=0)


def test_lookup():
    # For keys halfway between existing, tests will accept either value
    grenade = HandGrenade({
        4: 'four',
        8: 'eight',
        15: 'fifteen',
        16: 'sixteen',
        23: 'twenty-three',
        42: 'forty-two'
    })
    assert grenade[5] == 'four'
    assert grenade[6] in ('four', 'eight')  # 'eight'
    assert grenade[7] == 'eight'
    assert grenade[11] == 'eight'
    assert grenade[11.5] in ('eight', 'fifteen')  # 'eight'
    assert grenade[12] == 'fifteen'
    assert grenade[15] == 'fifteen'
    assert grenade[15.5] in ('fifteen', 'sixteen')  # 'sixteen'
    assert grenade[16] == 'sixteen'
    assert grenade[19] == 'sixteen'
    assert grenade[19.5] in ('sixteen', 'twenty-three')
    assert grenade[20] == 'twenty-three'
    assert grenade[32] == 'twenty-three'
    assert grenade[32.5] in ('twenty-three', 'forty-two')
    assert grenade[33] == 'forty-two'


def test_new_keys():
    grenade = HandGrenade({0: 'zero'})
    assert grenade[5] == 'zero'
    grenade[8] = 'eight'
    assert grenade[5] == 'eight'
    grenade[4] = 'four'
    assert grenade[5] == 'four'
    grenade[5] = 'five'
    assert grenade[5] == 'five'


def test_pop():
    grenade = HandGrenade({
        4: 'four',
        8: 'eight',
        15: 'fifteen',
        16: 'sixteen',
        23: 'twenty-three',
        42: 'forty-two'
    })
    assert grenade[24] == 'twenty-three'
    assert grenade.pop(23) == 'twenty-three'
    assert grenade[24] == 'sixteen'
    assert grenade.pop(16) == 'sixteen'
    assert grenade[24] == 'fifteen'
    assert grenade.pop(15) == 'fifteen'
    assert grenade[24] == 'eight'
    assert grenade.pop(8) == 'eight'
    assert grenade[24] == 'forty-two'
    assert grenade.pop(42) == 'forty-two'
    assert grenade[24] == 'four'
    assert grenade.pop(4) == 'four'
    assert not grenade


def test_popitem():
    grenade = HandGrenade({
        1: 'one',
        2: 'two',
        3: 'three',
        5: 'five',
        8: 'eight'
    })
    items = list(grenade.items())
    while items:
        item = grenade.popitem()
        assert item in items
        items.remove(item)
    assert not grenade


def test_removal():
    grenade = HandGrenade({
        4: 'four',
        8: 'eight',
        15: 'fifteen',
        16: 'sixteen',
        23: 'twenty-three',
        42: 'forty-two'
    })
    assert grenade[17] == 'sixteen'
    del grenade[16]
    assert grenade[17] == 'fifteen'
    del grenade[15]
    assert grenade[17] == 'twenty-three'
    del grenade[23]
    assert grenade[17] == 'eight'
    del grenade[8]
    assert grenade[17] == 'four'
    del grenade[4]
    assert grenade[17] == 'forty-two'


def test_setdefault():
    grenade = HandGrenade(lower=-1, upper=1)
    with pytest.raises(KeyError):
        grenade.setdefault(2, 2)
    assert not grenade
    assert grenade.setdefault(0, 3) == 3
    assert grenade[1] == 3


def test_update():
    grenade = HandGrenade({
        1: 'one',
        3: 'three'
    }, lower=-1, upper=4)
    with pytest.raises(KeyError):
        grenade.update({-2: 'negative two'})
    with pytest.raises(KeyError):
        grenade.update({5: 'five'})
    assert grenade == HandGrenade({
        1: 'one',
        3: 'three'
    }, lower=-1, upper=4)
    grenade.update({
        0: 'zero',
        2: 'two'
    })
    assert grenade == HandGrenade({
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three'
    }, lower=-1, upper=4)
    grenade.update(HandGrenade({
        -1: 'negative one',
        4: 'four'
    }))
    assert grenade == HandGrenade({
        -1: 'negative one',
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four'
    }, lower=-1, upper=4)
