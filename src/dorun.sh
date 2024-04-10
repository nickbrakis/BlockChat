#!/bin/bash
docker rm -f $(docker ps -a -q)
docker network create -d bridge my_network
docker build -t blockchat .
for i in $(seq 0 $1)
do
  docker run --network=my_network --name container$i -d -p 800$i:8000 -e IP_ADDRESS=container$i -e BOOTSTRAP=container0 -e CAPACITY=$2 -e NUM_NODES=$1 blockchat
done  