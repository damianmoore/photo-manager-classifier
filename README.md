# photo-manager-classifier

This project provides a deep learning image auto-tagging classifier as a JSON REST API. It is intended to be used as part of [this project](https://github.com/damianmoore/photo-manager).

It currently uses Caffe2 and the squeezenet pre-trained model. In time I intend to transfer and train from a dataset that has more relevant categories and better accuracy. This could even be user contributed eventually.


## Setup

```
git clone git@github.com:damianmoore/photo-manager.git
cd photo-manager-classifier/
```
Edit the file `docker-compose.yml` to mount your directory of photos as the volume `/photos` then build and run.
```
docker-compose build
docker-compose up
```
It will take a while to build the Docker image as it is based off a large deep-learning image that is over 900MB to download. This can be reduced in future as we don't need all the included resources and trained models. It works for now as a means to get up and running.


## Querying

Once the server is running you should be able to use _curl_ or _HTTPie_ to issue requests, passing a path to a file in the mounted volume directory.

**curl**:
```
curl -H "Content-Type: application/json" -X GET -d '{"path": "/photos/IMG_6085.jpg"}' http://localhost:8888/categories/
```

**HTTPie**:
```
http GET localhost:8888/categories/ path='/photos/IMG_6085.jpg'
```


## Response

You should get a response (after a few seconds) like this:
```
{
    "categories": [
        [
            "acoustic guitar",
            0.4404420852661133
        ],
        [
            "rifle",
            0.07927235215902328
        ],
        [
            "bannister, banister, balustrade, balusters, handrail",
            0.05965603142976761
        ],
    ],
    "path": "/photos/IMG_6085.jpg",
    "version": 0
}
```
