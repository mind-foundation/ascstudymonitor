""" Common interface for posting from a queue """

from ascmonitor.post_queue import PostQueue


class Poster:
    """ Posts documents to channels """

    def __init__(self, event_store):
        self.event_store = event_store
        self.queue = PostQueue(event_store)

    def post(self, channels):
        """
        Post the next document in queue
        :param channels: List of channels to post to
        """
