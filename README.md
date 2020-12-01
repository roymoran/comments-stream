## Comment Stream
Stream comments posted on social platforms in near-real time and persist them to queue for processing.

## Currently Supported
- Reddit

## Build and Run

```bash 
# from repo root
# build image
$ docker build -t comments-stream -f ci/Dockerfile .

# run container
$ docker run -d --name comments-stream -e REDDIT_CLIENT_ID="6PIAxTxBybD3cQ" REDDIT_CLIENT_SECRET="QEIog1oX_8JjUsQYzg8GYAmtQSq0tQ" comments-stream 

# remove image done
$  docker rm -f comments-stream
```