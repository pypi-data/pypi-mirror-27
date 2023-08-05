async-connect.py
================

.. image:: https://img.shields.io/pypi/v/async-connect.py.svg
   :target: https://pypi.python.org/pypi/async-connect.py
.. image:: https://img.shields.io/pypi/pyversions/async-connect.py.svg
   :target: https://pypi.python.org/pypi/async-connect.py
.. image:: https://travis-ci.org/GiovanniMCMXCIX/async-connect.py.svg?branch=master
   :target: https://travis-ci.org/GiovanniMCMXCIX/async-connect.py
.. image:: https://discordapp.com/api/v7/guilds/119860281919668226/embed.png?style=shield
   :target: https://discord.gg/u5F8y9W

async-connect.py is the asynchronous version of `connect.py <https://github.com/GiovanniMCMXCIX/connect.py>`__

If you want to report errors, bugs or typos you can join the discord guild listed next to the build shield.

Installing
----------

To install the library, you can just run the following command:

.. code:: sh

    python3 -m pip install -U async-connect.py

To install the development version, do the following:

.. code:: sh

    python3 -m pip install -U https://github.com/GiovanniMCMXCIX/async-connect.py/archive/master.zip#egg=async-connect.py[performance]

Requirements
------------

* Python 3.6+
* ``aiohttp`` library

Extra Requirements
------------------

This library contains an extra requirement that is name ``performance`` in other the library to work faster.
You can install it using the following command:

.. code:: sh

    python3 -m pip install -U async-connect.py[performance]

Note for using ``uvloop`` on async-connect.py you need to parse it to ``connect.Client()`` like so:

.. code:: py

    import asyncio
    import uvloop
    import async_connect as connect

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    client = connect.Client(loop=loop)

    # rest of your code here

Example
-------

.. code:: py

    import async_connect as connect

    async def get_release():
        releases = await client.search_release('friends')
        print('Found the following:')
        for release in releases:
            print('{0.title} by {0.artists} [{0.catalog_id}] was released on {0.release_date} '
                  'and has {1} track(s)'.format(release, len(await release.tracks.values())))

    if __name__ == "__main__":
        client = connect.Client()
        client.loop.run_until_complete(get_release())

