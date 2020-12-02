import os
import praw

APP_VERSION = 'v0.1.0'
reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'], user_agent=f'python3.8:{APP_VERSION} (by /u/bookfinderbot)')
subreddit = 'all'
comments = []

def stream():
    for comment in reddit.subreddit(subreddit).stream.comments():
        print("-------------New Comment--------------")
        print(comment.body)
        comments.append(comment.body)
        print(len(comments))
    


stream()
