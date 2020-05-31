""" A channel to twitter """

import tweepy
from tweepy import TweepError
from flask import url_for

from ascmonitor import DocumentType
from ascmonitor.channels import Channel, PreparedPost, SentPost, PostSendException


class TwitterChannel(Channel):
    """ Twitter Channel """

    name = "twitter"  # short name

    character_limit = 280
    space_for_hashtags = 100
    templates = [
        "{title}. {first_name} {last_name} et.al.",
        "{title}. {initial_name}. {last_name} et.al.",
        "{title}. {initial_name} {last_name} et.al.",
        "{title}. {last_name} et.al.",
        "{title_short}... {initial_name} {last_name} et.al.",
        "{title}.",
        "{title_short}...",
    ]
    static_hashtags = ["science"]

    def __init__(self, api_key, api_secret, access_token, access_secret):
        """ Connect to twitter """
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)
        self.twitter = tweepy.API(auth)
        self.twitter.verify_credentials()

    @staticmethod
    def extract_author(document):
        """ Get author information reliably """
        names = {"first_name": "", "last_name": "", "initial_name": ""}
        authors = document.get("authors", [])
        if not authors:
            return names

        author = authors[0]

        if "last_name" not in author:
            # no last name -> no author
            return names

        names["last_name"] = author["last_name"]

        if "first_name" in author:
            first_name = author["first_name"]
            if first_name.endswith("."):
                first_name = first_name[:-1]
            names["first_name"] = first_name
            names["initial_name"] = first_name[0].upper()

        return names

    @staticmethod
    def get_url(document):
        """ Build tweet url for document """
        return url_for("publication", slug=document["slug"])

    def format(self, document: DocumentType) -> PreparedPost:
        """ Format a document to return a post """
        templates = [*self.templates]

        title = document["title"]
        title_short = " ".join(title[:100].split(" ")[:-1])

        # extract author and remove invalid templates
        author = self.extract_author(document)
        missing = {k for k, v in author.items() if not v}
        templates = [t for t in templates if not any(k in t for k in missing)]

        # find a headline
        for template in templates:
            status = template.format(title=title, title_short=title_short, **author)
            if len(status) <= self.character_limit - self.space_for_hashtags:
                break
        else:
            raise PostSendException(
                "Could not find format fitting headline character limit: "
                f"id={document['id']} - title={title}",
                allow_retry=False,
            )

        hashtags = (
            self.static_hashtags + document.get("disciplines", []) + document.get("keywords", [])
        )
        for hashkw in hashtags:
            hashtag = f" #{hashkw}"
            if len(status) + len(hashtag) > self.character_limit:
                break
            status += hashtag

        return PreparedPost(
            document=document,
            channel=self,
            payload={"status": status, "attachment_url": self.get_url(document)},
        )

    def send(self, post: PreparedPost) -> SentPost:
        """ Send a post via a channel """
        try:
            status = self.twitter.update_status(**post.payload)
            post_id = status.id_str
            created = status.created_at
            hashtags = status.entities["hashtags"]
            urls = status.entities["urls"]
            return SentPost.from_prepared(
                post, id_=post_id, created=created, response={"hashtags": hashtags, "urls": urls},
            )

        except TweepError as error:
            msg = f"{error.reason}"
            raise PostSendException(msg, allow_retry=False)
