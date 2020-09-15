""" A channel to twitter """

from datetime import datetime, timedelta
import logging
import re

import tweepy
from tweepy import TweepError
from flask import request, url_for

from ascmonitor.channels import Channel, PreparedPost, SentPost, PostSendException
from ascmonitor.config import development
from ascmonitor.types import PublicationType

logger = logging.getLogger(__name__)


class TwitterChannel(Channel):
    """ Twitter Channel """

    name = "twitter"  # short name

    character_limit = 280
    space_for_hashtags = 100

    templates = [
        "{title}\n{first_name} {last_name} et al",
        "{title}\n{initial_name}. {last_name} et al",
        "{title}\n{last_name} et al",
        "{title_short}\n{initial_name} {last_name} et al",
        "{title}",
        "{title_short}",
    ]
    static_hashtags = [
        "PsychedelicResearch",
        "Psychedelic",
        "Science",
        "AcademicTwitter",
    ]

    def __init__(self, api_key, api_secret, access_token, access_secret):
        """ Connect to twitter """
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)
        self.twitter = tweepy.API(auth)
        self.twitter.verify_credentials()

        self.update_short_url_length()

    def update_short_url_length(self):
        """ Update the twitter shortened link length """
        try:
            config = self.twitter.configuration()
            self._short_url_length_https = config["short_url_length_https"]
        except tweepy.error.RateLimitError:
            self._short_url_length_https = 23
        self._short_url_length_https_expiry = datetime.now() + timedelta(days=1)

    @property
    def short_url_length_https(self):
        """ Update the config if necessary """
        if datetime.now() > self._short_url_length_https_expiry:
            self.update_short_url_length()
        return self._short_url_length_https

    @staticmethod
    def extract_author(publication):
        """ Get author information reliably """
        names = {"first_name": "", "last_name": "", "initial_name": ""}
        authors = publication.get("authors", [])
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
    def get_url(publication):
        """ Build tweet url for publication """
        if development:
            host = request.host_url
            return host + url_for("publication", slug=publication["slug"])
        return url_for("publication", slug=publication["slug"], _external=True)

    def format(self, publication: PublicationType) -> PreparedPost:
        """ Format a publication to return a post """
        templates = [*self.templates]

        title = publication["title"]
        title_short = " ".join(title[:100].split(" ")[:-1]) + "…"

        # extract author and remove invalid templates
        author = self.extract_author(publication)
        missing = {k for k, v in author.items() if not v}
        templates = [t for t in templates if not any(k in t for k in missing)]

        # find a headline
        space_for_headline = (
            self.character_limit
            - self.space_for_hashtags
            - self.short_url_length_https
            - 1
        )
        for template in templates:
            status = template.format(title=title, title_short=title_short, **author)
            if len(status) <= space_for_headline:
                break
        else:
            raise PostSendException(
                "Could not find format fitting headline character limit: "
                f"id={publication['id']} - title={title}",
                allow_retry=False,
            )

        status += "\n{url}\n\n"

        keywords = [
            kw
            for kw in publication.get("keywords", [])
            if kw not in self.static_hashtags
        ]
        hashtags = self.static_hashtags + publication.get("disciplines", []) + keywords
        for hashkw in hashtags:
            if " " in hashkw:
                hashkw = hashkw.title()
            hashkw = re.sub(r"\W", "", hashkw)
            hashtag = f" #{hashkw}"

            # win 5 and loose x chars by replacing {url}
            if (
                len(status) + len(hashtag)
                > self.character_limit + 5 - self.short_url_length_https
            ):
                break
            status += hashtag

        status = status.format(url=self.get_url(publication))

        logger.debug("Prepared post %s, length %d", status, len(status))
        return PreparedPost(publication=publication, channel=self, payload=status)

    def send(self, post: PreparedPost) -> SentPost:
        """ Send a post via a channel """
        try:
            status = self.twitter.update_status(status=post.payload)
            post_id = status.id_str
            created = status.created_at
            hashtags = status.entities["hashtags"]
            urls = status.entities["urls"]
            return SentPost.from_prepared(
                post,
                id_=post_id,
                created=created,
                response={"hashtags": hashtags, "urls": urls},
            )

        except TweepError as error:
            raise PostSendException(error.reason, allow_retry=False) from error
