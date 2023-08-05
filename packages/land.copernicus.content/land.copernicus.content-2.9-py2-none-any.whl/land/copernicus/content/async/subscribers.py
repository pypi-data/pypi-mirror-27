""" Subscribers
"""
import os
import logging
from plone.app.async.subscribers import set_quota
logger = logging.getLogger('land.copernicus.content')


NAME = 'landfiles'


def get_maximum_threads(queue):
    """ Get the maximum threads per queue
    """
    size = 0
    for dispatcher_agent in queue.dispatchers.values():
        if not dispatcher_agent.activated:
            continue
        for _agent in dispatcher_agent.values():
            size += 3
    return size or 1


def configure_queue(event):
    """ Configure zc.async queue for land files async jobs
    """
    queue = event.object
    size = get_maximum_threads(queue)
    set_quota(queue, NAME, size=size)

    logger.info(
        "quota %s with size %r configured in queue %r.",
        NAME,
        size,
        queue.name,
    )
