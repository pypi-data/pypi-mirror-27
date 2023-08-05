influxdbpusher
==============

.. image:: https://img.shields.io/pypi/v/influxdbpusher.svg
    :target: https://pypi.python.org/pypi/influxdbpusher
    :alt: Latest PyPI version

Minimal and smart pusher of samples to InfluxDB for asyncio programs

Usage
-----

1. Create a ``InfluxDbPusher`` object
2. Call it to push samples
3. ``InfluxDbPusher`` will try to do intelligent aggregation of samples in the
   background to minimise the number of HTTP request to the InfluxDb server.

Example:

.. code-block:: python

	import asyncio
	import logging
	from influxdbpusher import InfluxDbPusher


	async def test():
	    logging.basicConfig(level=logging.DEBUG)
	    influx = InfluxDbPusher("http://influxdb:8086", "playground")
	    while True:
	        for dummy in range(10):
	            await asyncio.sleep(0.02)
	            influx("test", dummy, {"foo": "bar"})
	            influx("measurement1",
	                   {"fieldname1": 'hello "world"', "value": 2.0},
	                   {"foo": "bar"})
	        await asyncio.sleep(5)
	    await influx.close()


	if __name__ == '__main__':
	    asyncio.get_event_loop().run_until_complete(test())


Installation
------------
.. code-block:: bash

	pip install influxdbpusher


Requirements
^^^^^^^^^^^^

Python >= 3.5

Compatibility
-------------

Licence
-------

MIT License

Copyright (c) 2017, Gambit Research

Authors
-------

`influxdbpusher` was written by `Gustavo Carneiro <gjcarneiro@gmail.com>`_.


