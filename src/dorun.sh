docker rm -f $(docker ps -a -q)
docker network create -d bridge my_network
docker build -t blockchat .
for i in {0..1}
do
  docker run --network=my_network -d -p 800$i:8000 -e IP_ADDRESS=127.0.0.1 -e PORT=800$i -e BOOTSTRAP=127.0.0.1 -e BOOTSTRAP_PORT=8000 blockchat
done  