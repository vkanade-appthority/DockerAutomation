#!/usr/bin/env bash
set -e
BASE_IMAGE="registry"
REGISTRY="registry.hub.docker.com"
IMAGE="$REGISTRY/$BASE_IMAGE"
CID=$(docker ps | grep $IMAGE | awk '{print $1}')
docker pull $IMAGE

for im in $CID
do
    LATEST=`docker inspect --format "{{.Id}}" $IMAGE`
    RUNNING=`docker inspect --format "{{.Image}}" $im`
    NAME=`docker inspect --format '{{.Name}}' $im | sed "s/\///g"`
    echo "Latest:" $LATEST
    echo "Running:" $RUNNING
    if [ "$RUNNING" != "$LATEST" ];then
        echo "upgrading $NAME"
        stop docker-$NAME
        docker rm -f $NAME
        start docker-$NAME
    else
        echo "$NAME up to date"
    fi
done



# init with => docker update-running -t -i --name $NAME $im /bin/bash
# Console accessible at:  http://54.191.69.59/

# [4:01] 
# Credentials:  User: admin@appthority.com, Password: admin

# [4:04] 
# docker pull appthority/connector
# docker run --name mdm-connector-container -e ORG_ID=884 -e AUTH_TOKEN=qTm8v6aRipCXZdNgjy3y appthority/connector

# [4:07] 
# docker pull appthority/connector
# docker run --name mdm-connector-container -d -e ORG_ID=884 -e AUTH_TOKEN=qTm8v6aRipCXZdNgjy3y appthority/connector