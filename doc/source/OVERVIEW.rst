========
Overview
========

There are several modules, which working separately from each other:


- :mod:`queue_manager` module
    manage (hostname, source) and result

- :mod:`input_worker` module
    responsible for putting (hostname, source) to the manager

- :mod:`sslyze_worker` module
    getting hostname from manager, analyze the SSL configuration of the server and putting result to the manager

- :mod:`result_worker` module
    getting (result, source) from manager, format it and make it persistent

|
| It is still not clear to you how it works? Lets see the graph:
|
|


.. figure::  _static/schema.jpg
