HandGrenade: the Python dict where close counts
===============================================
HandGrenade is a dict with numeric keys that allows lookup through nearby values. I decided not to call it horseshoe.

Basic Use
~~~~~~~~~
When given a key not defined, HandGrenade returns the value corresponding to the numerically closest defined key.

.. code-block:: python

    >>> from hand_grenade import HandGrenade
    >>> grenade = HandGrenade({0: 'zero', 12: 'twelve'})
    >>> grenade
    HandGrenade({0: 'zero', 12: 'twelve'}, lower=-inf, upper=inf)
    >>> grenade[0]
    'zero'
    >>> grenade[5]
    'zero'
    >>> grenade[7]
    'twelve'
    >>> grenade[12]
    'twelve'
HandGrenade also supports the usual dict methods, such as adding/removing/updating items.

.. code-block:: python

    >>> grenade[7] = 'seven'
    >>> grenade[11] = 'eleven'
    >>> del grenade[12]
    >>> grenade
    HandGrenade({0: 'zero', 7: 'seven', 11: 'eleven'}, lower=-inf, upper=inf)
    >>> grenade[5]
    'seven'
    >>> grenade[12]
    'eleven'
Lower and Upper Bounds
~~~~~~~~~~~~~~~~~~~~~~
If such a feature is desired, HandGrenade allows one to limit the range allowed for its keys. On an attempt to access a key out of the acceptable range, or upon an access to an empty HandGrenade, a KeyError is thrown. This includes the keys in the dict used to construct HandGrenade.

.. code-block:: python

    >>> HandGrenade({0: 24}, lower=12)
    Traceback (most recent call last):
    ...
    KeyError: '0'
    >>> HandGrenade()[3]
    Traceback (most recent call last):
    ...
    KeyError: '3'
    >>> grenade = HandGrenade({7: 11}, lower=6, upper=8)
    >>> grenade[5]
    Traceback (most recent call last):
    ...
    KeyError: '5'
    >>> grenade[8] = 3
    >>> grenade[9] = 4
    Traceback (most recent call last):
    ...
    KeyError: '9'

.. note::

    Currently, HandGrenade does not support changing bounds after creation. If anyone wants this, `create an issue <https://github.com/brettbeatty/hand_grenade/issues>`_.
Midpoints
~~~~~~~~~
The midpoints between two adjacent keys should be considered uncertain. Currently, which key is chosen depends on the key's position in HandGrenade's underlying search tree. Therefore, one should expect one of the two nearby keys to be chosen without guarantees as to which.

.. code-block:: python

    >>> grenade = HandGrenade({-2: 4, 2: 6})
    >>> assert grenade[0] in {4, 6}
