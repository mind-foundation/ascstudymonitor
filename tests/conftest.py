import os

# setup environment for testing
os.environ["FLASK_ENV"] = "development"
os.environ["POST_SECRET_TOKEN"] = "post_secret_token_test"
os.environ["MENDELEY_CLIENT_ID"] = "test"
os.environ["MENDELEY_CLIENT_SECRET"] = "xxx"
os.environ["MENDELEY_REDIRECT_URI"] = "http://example.com"
os.environ["MENDELEY_USER"] = "xxx"
os.environ["MENDELEY_PASSWORD"] = "xxx"
os.environ["TWITTER_API_KEY"] = "xxx"
os.environ["TWITTER_API_SECRET"] = "xxx"
os.environ["TWITTER_ACCESS_TOKEN"] = "xxx"
os.environ["TWITTER_ACCESS_SECRET"] = "xxx"
