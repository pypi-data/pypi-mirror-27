Using local time in Python2 logging
===================================

Python 2 logging module doesn't support using a timezone offset ``%z`` in the datetime format string.  An example failure mode is shown below:

.. code-block:: python

   import logging
   datefmt = '%Y-%m-%d %H:%M:%S%z'
   logging.basicConfig(format='%(asctime)s %(message)s', datefmt=datefmt)
   logging.warning("Dude, where's my tzinfo?")  # it's about 6.20 pm here in Chicago
   # 2017-02-27 18:23:05+0000 Dude, where's my tzinfo?
                        ^^^^^

Simply omitting the time zone offset would perhaps have been admissible, or perhaps even simply refusing to localize and just logging in UTC, but specifying the localized time **and** specifying a zero offset is certainly wrong.  The part marked ``^`` is incorrect, an offset timestamp should have looked more like this one:

.. code-block:: python

   import pytz
   from datetime import datetime
   chicago_now = datetime.now(tz=pytz.timezone('America/Chicago'))
   print chicago_now.strftime(datefmt)
   # 2017-02-27 18:23:13-0600

Indeed, that's how the logging output *does* look if run under Python 3.  But in Python 2, the ``%z`` directive is dropped.  This module provides a ``LocalFormatter`` intended as a drop-in replacement, to provide the correct handling of time zone offsets under Python 2:

.. code-block:: python

   import logging, logging_tz
   datefmt = '%Y-%m-%d %H:%M:%S%z'
   logger = logging.getLogger('wat')
   handler = logging.StreamHandler()
   formatter = logging_tz.LocalFormatter(fmt='%(asctime)s %(message)s', datefmt=datefmt)
   handler.setFormatter(formatter)
   logger.addHandler(handler)
   logger.warning("Ah, there's my tzinfo!")
   # 2017-02-27 18:25:53-0600 Ah, there's my tzinfo!

Additionally a ``ChicagoFormatter`` is offered as a convenience, to ease the pain for anyone insane enough to run their backend on CST instead of UTC.


FAQ
---

Q:
  How to install this library?
A:
  ``pip install logging_tz`` and then you can just use a ``logging_tz.LocalFormatter`` instead of the ``logging.Formatter``.


Q:
  You should log in UTC.  Why would you log in local time anyway?
A:
  `Yeah, I guess <http://yellerapp.com/posts/2015-01-12-the-worst-server-setup-you-can-make.html>`_.  Although handling the date format correctly is at least better than mucking it up completely.


Q:
  Is that a bug in Python?
A:
  Hmm, arguably not, because the ``%z`` directive for time zone offset is not listed on the ``time.strftime`` table in the `Python 2 documentation <https://docs.python.org/2/library/time.html#time.strftime>`_.  It is `there in the Python 3 docs <https://docs.python.org/3/library/time.html#time.strftime>`_, though.


Q:
  Did people really ask you these questions?  I bet you just made them up for the FAQ.
A:
  That's a very good question - it's one I've frequently asked myself, in fact.


