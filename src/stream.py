import os
import praw
from prawcore import ServerError
from src.const import APP_VERSION

reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'], user_agent=f'python3.8:{APP_VERSION} (by /u/bookfinderbot)')
subreddit = 'all'


def stream_generator():
    try:
        for comment in reddit.subreddit(subreddit).stream.comments():
            yield comment
    except praw.exceptions.RedditAPIException as exception:
        print('Exception while fetching latest comments. Reddit might be down. Check https://www.redditstatus.com/.')
        print(exception)
    except ServerError as exception:
        print('Exception while fetching latest comments. Reddit might be down. Check https://www.redditstatus.com/.')
        print(exception)
