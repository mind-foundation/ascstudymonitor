"""
Keep track of changes to the document store
and posted publications.
"""


class EventStore:
    """ Put and query events to an event log """

    def __init__(self, db, document_store):
        """ Connect the event store to the database """

    def put(self, event):
        """ Put an event in the event store """

    def query(self, filter_=None):
        """
        Iterate events filtered by event kinds,
        starting with the newest
        """
