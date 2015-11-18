=====
Usage
=====

**For quick use, start "hft_tls_crawler.py" script, which starts all necessary worker processes in the correct order:**

::

    $ python hft_tls_crawler.py

**or start each component separately:**

- start the server (queue manager)

::

    $ python queue_manager.py

- start input worker to fill the queues

::

    $ python input_worker.py

- start sslyze worker

::

    $ python sslyze_worker.py

- start result worker

::

    $ python result_worker.py



