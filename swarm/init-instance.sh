NM=$1
MEM_RAM=${2:-1024M}
multipass launch --name ${NM} focal -m ${MEM_RAM}
multipass transfer setup-instance.sh ${NM}:/home/ubuntu/setup-instance.sh
multipass exec ${NM} -- sh -x ./setup-instance.sh
# https://techsparx.com/software-development/docker/swarm/multipass.html
# multipass exec swarm1 -- docker swarm join-token manager