# SLS Simple Load Simulator
### Pipeline: 25
#### curl  -H "Content-Type: application/json"  -X POST --data @data.json http://localhost:5000/worker <- worker
#### sudo docker run --name worker --net=bridge -d worker:1.0.2
#### sudo docker inspect worker | grep IPAddress
#### sudo docker stop worker
#### sudo docker rm worker

#### sudo docker run --name inf -d -t inf
#### sudo docker exec -it inf /bin/bash 

### 1. Install Terraform
```sh
{
    sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
    sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    sudo apt-get update && sudo apt-get install terraform -y
}
```
### 2. Install additional packages
```sh
{
sudo apt install make rsync -y

}
```
