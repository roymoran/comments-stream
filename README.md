## Comment Stream

Find comments of interests on social platforms by using a classifier trained on data that you collect.
## Platforms Currently Supported

- Reddit
## Dependencies 
- [Docker](https://docs.docker.com/engine/install/)

## Setup Reddit App Variables

Start by creating a new reddit app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).

```bash
# from repo root, create docker-compose.env 
# on windows manually create this file in ci directory and 
# copy contents of docker-compose.env.example into it
$ cp ci/docker-compose.env.example ci/docker-compose.env
```
Now update `docker-compose.env` with reddit app credentials generated 
## Collect Comments for Training/Testing Dataset

```bash
# from repo root
# build collector image
$ docker build -t comments-collector -f ci/collector.Dockerfile .

# run container and pass keywords (on windows replace $(pwd) with %cd%)
$ docker run -it --name comments-collector -v $(pwd)/documents:/usr/src/app/src/documents --env-file ci/docker-compose.env comments-collector key_word1 key_word2 key_word3

# remove container when done
$ docker rm -f comments-collector
```
### Demo
![Collector Demo](./docs/collector_demo.gif)

## Build and Run Classifier

```bash
# from repo root
# docker compose up
$ docker-compose --file ci/docker-compose.yml up -d
# rebuild images on changes
$ docker-compose --file ci/docker-compose.yml build
# when done
$ docker-compose --file ci/docker-compose.yml down
```

Start `custom.py` to view print out of valid comments. You can optionally modify `custom.py` to add custom logic for processing these comments (e.g. auto-replying or additional filtering). 

```bash
# from repo root
# build custom script image
$ docker build -t custom-script -f ci/custom.Dockerfile .
# run customer script container interactively
$ docker run -it --name custom-script --network ci_default custom-script
# remove container when done
$ docker rm -f custom-script
```

### Demo
![Classifier Demo](./docs/classifier_demo.gif)