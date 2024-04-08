docker rm -f $(docker ps -a -q)
docker network create -d bridge my_network
docker build -t blockchat .
for i in {0..4}
do
  docker run --network=my_network --name container$i -d -p 800$i:8000 -e IP_ADDRESS=container$i -e PORT=800$i -e BOOTSTRAP=container0 -e BOOTSTRAP_PORT=8000 blockchat
done  