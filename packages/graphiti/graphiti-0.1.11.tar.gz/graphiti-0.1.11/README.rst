========
Graphiti
========

**Graphiti** is python module for sending any metrics to `graphite/carbon <http://graphite.wikidot.com/>`_

Build status: |build_status|

.. |build_status| image::
  https://drone.io/bitbucket.org/asdtech/graphiti/status.png

Features
--------

* Asynchronous sending
* Combine several metrics to single packet
* Uses pickle protocol
* Handle temporary network outage
* Gevent support


Installation
============

**graphiti** is installed via pip.

   pip install graphiti



Usage Example
=============
Sample::

   from graphiti import Client

   client = Client(carbon_host)
   client.send("graphiti.server.cpu_usage", 12.4, timestamp)
   client.send("graphiti.server.cpu_usage", 15.1)  # current time will be used

   project = "graphite"
   server = "server"
   client.send((project, server, "cpu_usage"), 11)  # metric name is graphiti.server.cpu_usage


   # also you can aggregate values on client side
   from graphiti import Aggregator, timeit

   aggregator = Aggregator(client, interval=60)  # aggregate metrics during minute

   aggregator.add_sum('processed_messages', 1)
   aggregator.add_avg('message_processing_avg_time', time_taken)
   aggregator.add_active('service_is_up')

   with timeit(aggregator, ["graphiti", "server", "messages"]):
      process_message()  #  send metrics graphiti.server.messages.time_avg -- average time of message processing
                         #               graphiti.server.messages.time_sum -- total time of message processing
                         #               graphiti.server.messages.count -- number of processed message per minute

   client.stop()


Source
======
The **Graphiti** sources are hosted on bitbucket: https://bitbucket.org/asdtech/graphiti
