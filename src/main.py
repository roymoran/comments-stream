import praw

reddit = praw.Reddit(client_id="6PIAxTxBybD3cQ",
                     client_secret="QEIog1oX_8JjUsQYzg8GYAmtQSq0tQ", user_agent="my user agent")
subreddit = 'all'

def stream():
    for comment in reddit.subreddit(subreddit).stream.comments():
        print(comment)

stream()