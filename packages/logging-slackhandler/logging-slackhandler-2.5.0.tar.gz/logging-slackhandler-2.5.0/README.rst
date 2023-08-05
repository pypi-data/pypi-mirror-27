logging-slackhandler
====================

|Version| |Status| |Python| |License| |Build| |Thanks|

Introduction
------------

This module provides additionals handler, formatter and filter for the logging
package, so you can send Python log records to a Slack Incoming Webhook.

Credits
-------

This module is widely inspired by `Junhwi Kim <https://github.com/junhwi>`_'s
work on `python-slack-logger <https://github.com/junhwi/python-slack-logger>`_.

How it works
------------

In order to send records to Slack without slowing down code run, messages are
posted in background by a threads pool, while new records are added to the
queue.

In case of network delays or disconnection, app execution while not be blocked
waiting for post response.

Installation
------------

You can install, upgrade or uninstall logging-slackhandler using pip:

.. code-block:: bash

    pip install logging-slackhandler
    pip install --upgrade logging-slackhandler
    pip uninstall logging-slackhandler

Usage
-----

SlackHandler
~~~~~~~~~~~~

``SlackHandler`` instances dispatch logging events to Slack Incoming Webhook.

Here is the list of its parameters:

    :webhook_url: Slack Incoming Webhook URL.
    :username: (optional) message sender username.
    :channel: (optional) Slack channel to post to.
    :icon_emoji: (optional) customize emoji for message sender.
    :timeout: (optional) specifies a timeout in seconds for blocking operations.
    :pool_size: (optional) specifies number of workers processing records queue.

The following example shows how to send records to a Slack Incoming Webhooks:

.. code-block:: python

    import logging
    from SlackLogger import SlackHandler

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    slack_handler = SlackHandler('YOUR_WEBHOOK_URL')
    logger.addHandler(slack_handler)

    for level in ['debug', 'info', 'warning', 'error', 'critical']:
        getattr(logger, level)('This is a `%s` message', level)

SlackFormatter
~~~~~~~~~~~~~~

``SlackFormatter`` instances format log record and return a dictionary that can
be sent as a Slack message attachment.

Here is the list of its parameters:

    :attr: (optional) custom attachment parameters to record attributes dictionary.
    :lvl_color: (optional) custom record levels to colors dictionary.

You can customize the appearance of Slack message with ``attr`` parameter, to bind a
`Slack attachment property <https://api.slack.com/docs/message-attachments#attachment_structure>`_
to a record attribute. Empty strings will not be displayed in message.

Also, ``lvl_color`` parameter let you customize color-coding messages, binding a record
levelname to an hex color code or Slack special codes (``good``, ``warning``, ``danger``).

.. code-block:: python

    from SlackLogger import SlackFormatter

    attr={'pretext': '*Look at me!*', 'title': ''}
    lvl_color={'INFO': 'good'}

    slack_handler.setFormatter(SlackFormatter(attr=attr, lvl_color=lvl_color))

    logger.info('Hi there!')

SlackFilter
~~~~~~~~~~~

``SlackFilter`` instances can be use to determine if the specified record is to
be sent to Slack Incoming Webhook.

Here is the list of its parameters:

    :allow: filtering rule for log record.

You can use ``SlackFilter`` to allow only some records to be sent. When
``SlackFilter`` is defined, records will not be sent to Slack unless you
explicitly ask it for by adding ``extra`` argument, as in following example:

.. code-block:: python

    from SlackLogger import SlackFilter

    logger.addFilter(SlackFilter())

    logger.debug('This is a debug message')
    logger.info('Hi there!', extra={'slack': True})

To have the opposite behavior (sent record by default), just set ``allow``
parameter to ``True`` when creating ``SlackFilter``:

.. code-block:: python

    from SlackLogger import SlackFilter

    logger.addFilter(SlackFilter(allow=True))

    logger.debug('This is a debug message', extra={'slack': False})
    logger.info('Hi there!')

Good to know
------------

Messages order
~~~~~~~~~~~~~~

Messages are processed in a FIFO order from the queue, but due to network
latency, Slack response time or message length, concurrent messages can appear
in a different order in destination channel than the one you sent them.

If message order is a requirement, you can define SlackHandler with a pool size
of 1, so that only one thread will process the queue:

.. code-block:: python

    slack_handler = SlackHandler('YOUR_WEBHOOK_URL', pool_size=1)

License
-------

Copyright (c) 2017 Damien Le Bourdonnec

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

.. |Version| image:: https://img.shields.io/pypi/v/logging-slackhandler.svg?colorB=ee2269
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: Package Version
.. |Status| image:: https://img.shields.io/pypi/status/logging-slackhandler.svg
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: Development Status
.. |Python| image:: https://img.shields.io/pypi/pyversions/logging-slackhandler.svg?colorB=fcd20b
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/logging-slackhandler.svg
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: License
.. |Build| image:: https://img.shields.io/travis/Greums/logging-slackhandler.svg
    :target: https://travis-ci.org/Greums/logging-slackhandler
    :alt: Build Status
.. |Thanks| image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/inbox#badge-modal
    :alt: Say Thanks!
