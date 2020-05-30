from ascmonitor.channels import Channel, Post, PostSendException


class TwitterPost(Post):
    """ A tweet """


class TwitterChannel(Channel):
    """ Twitter Channel """

    def __init__(self, twitter):
        """ Connect to twitter """

    def format(self, document) -> TwitterPost:
        """ Format a document to return a post """

    def send(self, post: TwitterPost):
        """ Send a post via a channel """
