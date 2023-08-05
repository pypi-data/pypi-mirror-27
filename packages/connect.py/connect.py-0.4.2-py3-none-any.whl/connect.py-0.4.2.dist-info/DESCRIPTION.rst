connect.py
==========

.. image:: https://img.shields.io/pypi/v/connect.py.svg
   :target: https://pypi.python.org/pypi/connect.py
.. image:: https://img.shields.io/pypi/pyversions/connect.py.svg
   :target: https://pypi.python.org/pypi/connect.py
.. image:: https://travis-ci.org/GiovanniMCMXCIX/connect.py.svg?branch=master
   :target: https://travis-ci.org/GiovanniMCMXCIX/connect.py
.. image:: https://discordapp.com/api/v7/guilds/119860281919668226/embed.png?style=shield
   :target: https://discord.gg/u5F8y9W

connect.py is an API wrapper for `Monstercat Connect <https://www.monstercat.com/dev/api/connect>`__ written in Python.

If you want to report errors, bugs or typos you can join the discord guild listed next to the build shield.

Installing
----------

To install the library, you can just run the following command:

.. code:: sh

    python3 -m pip install -U connect.py

To install the development version, do the following:

.. code:: sh

    python3 -m pip install -U https://github.com/GiovanniMCMXCIX/connect.py/archive/master.zip#egg=connect.py[performance]

Requirements
------------

- Python 3.6+
- ``requests`` library

Extra Requirements
------------------

This library contains an extra requirement that is name ``performance`` in other the library to work faster.

You can install it using the following command:

.. code:: sh

    python3 -m pip install -U connect.py[performance]

Example
-------

.. code:: py

    import connect

    client = connect.Client()


    def get_release():
        releases = client.search_release('friends')
        print('Found the following:')
        for release in releases:
            print('{0.title} by {0.artists} [{0.catalog_id}] was released on {0.release_date} '
                  'and has {1} track(s)'.format(release, len(release.tracks)))


    if __name__ == "__main__":
        get_release()


