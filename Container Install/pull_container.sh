#!/bin/bash

## Check if user is logged in
if [ "$logged_in" = false  ]; then
   echo "Please enter credentials to login"
   # Read username
   read -p "Username: " USER

   # Password for user
   read -s -p "Password for $USER: " PASS

   # login using the credentials shared above
   docker login —-username $USER  --password $PASS

   echo "Docker Login Successful"
   # user login
   logged_in = true
fi

echo "Logged in as $USER"

# Enter details of Image to download
read -p "Name of Image to download: " IMAGE_NAME

echo "Pulling image $IMAGE_NAME"

# pull the image from docker hub

docker pull $IMAGE_NAME

# stop any previous running container
echo "Stopping previous instances of $IMAGE_NAME"
docker stop mdm-connector-container
# remove any previous running container
echo "Removing the $IMAGE_NAME container"
docker rm mdm-connector-container

read -p "Organization ID: " _ORG_ID

# run the container
docker run -t --name mdm-connector-container --net=host -d -e ORG_ID=_ORG_ID -e AUTH_TOKEN=qTm8v6aRipCXZdNgjy3y -p 12345:12345 $IMAGE_NAME

