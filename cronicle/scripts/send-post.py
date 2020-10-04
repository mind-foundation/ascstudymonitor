#!/usr/bin/env python3
"""
Post a publication via the GraphQL API
"""

import json

import click
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def get_secret():
    """ Get the secret from somewhere """
    with open("/run/secrets/asc-secret") as f:
        secrets = json.load(f)
    return secrets["POST_SECRET_TOKEN"]


def get_gql_client(endpoint):
    """ Setup the graphql client """
    transport = RequestsHTTPTransport(
        url=endpoint,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    return client


@click.command()
@click.option("--endpoint", "-e", required=True, help="The url to the graphql endpoint")
@click.option("--channel", "-c", required=True, help="The channel to post to")
def main(endpoint, channel):
    """ Post a publication """
    secret = get_secret()
    client = get_gql_client(endpoint)

    query = gql(
        """
        mutation post($channel: String!, $secret: String!) {
          post(channel: $channel, secret: $secret) {
            success
            message
            publication
            created
            postPayload
            postID
            response {
              hashtags
              urls
            }
          }
        }
    """
    )
    variables = {"channel": channel, "secret": secret}

    result = client.execute(query, variable_values=variables)
    print(result)


if __name__ == "__main__":
    main()
