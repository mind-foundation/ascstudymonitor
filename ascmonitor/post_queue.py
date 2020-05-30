"""
Provides interface to a post queue built from the event store
"""


class PostQueue:
    """ Get the next post or view the queue """

    def __init__(self, event_store):
        """ Built a new post queue """
        self.event_store = event_store

    def view(self):
        """ List all documents in the queue """

    def pop(self):
        """ Return the next document in the queue """
