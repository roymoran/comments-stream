## Comment Stream
Stream comments posted on social platforms in near-real time and persist them to queue for processing.

## Currently Supported
- Reddit

## Collect Comments for Training/Testing Dataset
```bash 
# from repo root
# build collector image
$ docker build -t comments-collector -f ci/collector.Dockerfile .

# run container and pass keywords
$ docker run -it --name comments-collector -v $(pwd)/documents:/usr/src/app/src/documents --env-file ci/docker-compose.env comments-collector key_word1 key_word2 key_word3

# remove image done
$  docker rm -f comments-collector
```
## Build and Run

```bash 
# from repo root
# build  streamer image
$ docker build -t comments-stream -f ci/stream.Dockerfile .

# run container
$ docker run -d --name comments-stream -e REDDIT_CLIENT_ID="6PIAxTxBybD3cQ" -e REDDIT_CLIENT_SECRET="QEIog1oX_8JjUsQYzg8GYAmtQSq0tQ" comments-stream 

# remove image done
$  docker rm -f comments-stream
```