#!/bin/bash

if [ $# -eq 0 ]; then
    echo "the image tag was not supplied"
    exit
fi

IMAGE_NAME=isnewsworthy
IMAGE_TAG=$1

docker build . -t $IMAGE_NAME:$IMAGE_TAG

docker tag $IMAGE_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:$IMAGE_TAG

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com    
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:$IMAGE_TAG
