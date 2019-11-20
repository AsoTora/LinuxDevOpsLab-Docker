# docker

## basics

Command line commands:

https://docs.docker.com/engine/reference/commandline/rm/

### Containers

? A container is something quite similar to a virtual machine, which can be used to contain and execute all the software required to run a particular program or set of programs.
The container includes an operating system (typically some flavor of Linux) as base, plus any software installed on top of the OS that might be needed.

**container isolation**
The Docker container technology essentially achieves process-level isolation by leveraging the Linux kernel constructs, such as namespaces and cgroups, particularly, the namespaces
https://stackoverflow.com/questions/34820558/difference-between-cgroups-and-namespaces

Commands

```
docker build -t my-first-app .
docker images
docker run -d -P my-first-app
docker run -d -p 10080:8080 my-first-app
```

How can we know how many containers are running currently?
`docker ps`

How can we stop any of them? (it doesnt destroy them)
`docker stop id`

Remove:
`docker rm` or `docker kill`

Remove all stopped
`docker rm $(docker ps -a -q)`

### Images

Lifecycle:

`docker images` - shows all images;

`docker import` - creates an image from a tarball;

`docker build` - creates image from Dockerfile;

`docker commit` - creates image from a container, pausing it temporarily if it is running;

`docker rmi` - removes an image;

`docker load` - loads an image from a tar archive as STDIN, including images and tags;

`docker save` - saves an image to a tar archive stream to STDOUT with all parent layers, tags & versions;

Info:

`docker history` - shows history of image;

`docker tag` - tags an image to a name (local or registry).

## Tasks

### DAY 1

docker build -t 'color/green':1.0 - < Dockerfile
docker build -t 'color/blue':2.6 -f Dockerfile_blue .

simple dockerfile:

```
FROM centos:7
LABEL AUTHOR=ashvedau

#install httpd
RUN yum install -y httpd
COPY index.html /var/www/html/

#run httpd
CMD [“/usr/sbin/httpd”, “-D”, “FOREGROUND”]
EXPOSE 80
```

docker run -d -t -i centos /bin/bash

**pass args**

```
# args
ARG CENTOS_VERSION

# main
FROM centos:${CENTOS_VERSION}
LABEL AUTHOR=ashvedau

# install open-jdk
ARG JAVA_VERSION=11
RUN yum install -y java-${JAVA_VERSION}-openjdk
```

**pass multiple args**

docker build -t c7j180 --build-arg CENTOS_VERSION=7 --build-arg JAVA_VERSI
ON=1.8.0 .

**summary**

```
docker image ls
docker image rm

docker build [-t image_tag] [-f ./path/to/dockerfile] .
docker build --build-arg BASE_IMAGE=ubuntu:16.04 .

docker tag (old_id|old_tag) (new_tag)

docker pull ubuntu
docker push myweb/1.0
```

### DAY 2

##### part 1 -- containers

**working with containers**

```
docker run -d --restart=always --name restarter_1 busybox sleep 3
docker run -d --restart=on-failure:7 --name restarter_2 busybox sleep 3

# options first!!
docker run -d --name busy --user 1000:0 --group-add 1200 --workdir /data --env STUDENT=shvedau busybox sleep infinity
```

run command inside a container

`docker exec batman sh -c "echo 'andrei-shvedau' >> /data/student"`

health-checks: https://docs.docker.com/engine/reference/run/#healthcheck

`docker run -d --name tomcat-health --health-cmd 'curl localhost:8080' tomcat`

logs: https://docs.docker.com/engine/reference/commandline/logs/

`docker logs [opts] container`

**summary**

```
docker run -d myhttpd:1.0

docker run -P -d myhttpd:1.0
docker run -d -p 8081:80 --name h8081 myhttpd:1.0

docker run -d --restart=always --name sleeper centos sleep 5

docker run centos cat /etc/redhat-release
docker run -it centos bash

docker stop h8082
docker rm 014e5efa5ca9
docker rm $(docker stop $(docker ps -a -q))

docker run --user 1000:0 jenkins id
docker run --group-add 123 jenkins id

docker run --workdir /var/jenkins_home jenkins pwd
docker run -it -e MYVAR="My Variable" centos env | grep MYVAR

docker run -d --label app=web1 nginx

docker logs (container_name | container_id)


docker run -dt --log-driver=journald --name httpd httpd
journalctl -ab CONTAINER_NAME=httpd

```

#### part 2 -- volumes

**volumes**

mount file:
`docker run -d -p 10083:80 --mount type=bind,source="/root/index.html",target="/usr/shar /nginx/html/index.html" --name c10083 nginx`

using created volumes:
`docker run -d -p 10087:80 -v c10087_custom_volume:/usr/share/nginx/html --name c10087 nginx`

**summary**

```
docker run -d -p 80:80 -v /usr/share/nginx/html nginx
docker run -d -p 80:80 -v nginx_data:/usr/share/nginx/html nginx

docker run -d --name html_data -v /usr/share/nginx/html busybox sleep infinity
docker run -d --volumes-from html_data -p 81:80 nginx

docker volume create --name http-custom-data
docker volume ls
docker volume inspect http-custom-data
```

### Day 3

#### part 1 -- networks

docs:

https://docs.docker.com/engine/reference/commandline/network_connect/

commands:

```
docker network connect - Connect a container to a network;
docker network create - Create a network;
docker network disconnect - Disconnect a container from a network;
docker network inspect - Display detailed information on one or more networks;
docker network ls - List networks;
docker network prune - Remove all unused networks;
docker network rm - Remove one or more networks.
```

`docker info | grep Network`

info:

**maximum transmission unit (MTU)** -- the largest packet length that the container will allow, defaults to 1500 bytes.\*\*

- bridge: The default network driver. Bridge networks are usually used when your applications run in
  standalone containers that need to communicate.

- host: For standalone containers, remove network isolation between the container and the Docker host,
  and use the host’s networking directly.

- overlay: Overlay networks connect multiple Docker daemons together and enable swarm services to
  communicate with each other.

- macvlan: Macvlan networks allow you to assign a MAC address to a container, making it appear as a
  physical device on your network. Using the macvlan driver is sometimes the best choice when dealing
  with legacy applications that expect to be directly connected to the physical network, rather than routed
  through the Docker host’s network stack.

- null: For this container, disable all networking. Usually used in conjunction with a custom network driver.

run with host network:

`docker run -d --name=httpd_host --network=host httpd`
`docker run -d --name=nginx-ashvedau-bridge --network=ashvedau-bridge --label=createdby=andrei_shvedau nginx`

check container:

`docker inspect fef401c49023 | jq '.[].NetworkSettings.Networks'`
`docker inspect nginx-ashvedau-bridge | jq '.[].Config.Labels'`

connect containers:

`docker network create --driver=bridge --subnet=123.45.1.0/24 --ip-range=123.45.1.0/24 --label=createdby=andrei_shvedau ashvedau-bridge`
`docker network connect ashvedau-bridge alpine_ping`

**summary**

```
docker network ls
docker network inspect bridge

docker run --net=none -d --name inNoneContainer busybox
docker run -d --network=host --name=nginx nginx

docker run -d -it --name=my_container_1 busybox
docker run -d -it --name=my_container_2 busybox
docker network inspect bridge | jq '.[].Containers'

docker network create < network_name >
docker network create <options> <network>
docker network create --help

docker run -d --name=inmybridge1 --net=my_bridge_network centos sleep infinity
```

#### part 2 -- compose

https://github.com/AsoTora/LinuxDevOpsLab-Docker/tree/master/compose

### Day 4

#### part 1 -- Namespaces and Control Groups

**Cgroups** - limits how much you can use

Resource metering and limiting:

- memory
- CPU
- block I/O
- network
- Device node /dev/\* access control

**Namespaces** - limits what you can see (and therefore use)

- Provide processes with their own view of the system
- Multiple namespaces: - pid – isolates the process ID number space - net – manages network devices - mnt – to see distinct single- directory hierarchies - uts – isolating hostnames - ipc – manages shared memory areas, message queues, and semaphores
  Each process is in one namespace of each type

run with other container **namespace**:

`docker run -d --name=busy_sleep_inf --pid=container:nginx_pid busybox sleep infinity`

run with other container **NET**:

`docker run -dit --name=net-tools --net=container:nginx-net sbeliakou/net-tools`

**UTS**

`docker run -d --name=busy-host --uts=host busybox sleep infinity`

**Cgroups**

```
docker run -d --name=tomcat --memory 100M --memory-reservation 50M --memory-swap -1 tomcat:jdk8-openjdk-slim
docker run -dit --name cpu-stress --cpu-quota=20000 alpine md5sum /dev/urandom
```

**Summary**

```
docker run --rm --pid=container:web-conatiner centos ps

docker run -d -it --net=container:nginx sbeliakou/net-tools

docker run --rm --uts=host busybox hostname

docker run -d -m 300M --memory-reservation 100M centos sleep infinity

docker run -it -d --cpu-quota=25000 --name cpu0.25_1 alpine md5sum /dev/urandom
docker run -it -d --cpus=0.25 --name cpu0.25_2 alpine md5sum /dev/urandom
```

#### part 2 -- extra

Container Vulnerabilities. Anchore CLI. Scanning

```
anchore-cli image list
docker-compose exec engine-api anchore-cli image add docker.io/library/centos:latest
docker-compose exec engine-api anchore-cli image add docker.io/library/postgres:latest
docker-compose exec engine-api anchore-cli image add docker.io/library/nginx:latest

docker-compose exec engine-api anchore-cli image vuln docker.io/library/centos:latest os
docker-compose exec engine-api anchore-cli image vuln docker.io/library/postgres:latest os
docker-compose exec engine-api anchore-cli image vuln docker.io/library/nginx:latest os

```

delete:

`anchore-cli subscription deactivate tag_update docker.io/library/centos:7 anchore-cli subscription deactivate analysis_update docker.io/library/centos:7 anchore-cli image del docker.io/library/centos:7`

**dockerd configuration**

https://docs.docker.com/config/daemon/

{
"hosts": [
"tcp://0.0.0.0:2375",
"unix://var/run/dokcer.sock"
],
"live-restore": true,
"metrics-addr": "127.0.0.1:9323",
"expiremental": true
}

## links

https://medium.com/faun/how-to-build-a-docker-container-from-scratch-docker-basics-a-must-know-395cba82897b

**multi-stage**

https://medium.com/@tonistiigi/advanced-multi-stage-build-patterns-6f741b852fae

**containers**

run:

https://docs.docker.com/engine/reference/run/

restarts:

https://docs.docker.com/engine/reference/run/#restart-policies---restart

health:

https://blog.couchbase.com/docker-health-check-keeping-containers-healthy/

inspect:

https://docs.docker.com/machine/reference/inspect/

**volumes**
https://docs.docker.com/storage/volumes/
https://docs.docker.com/storage/bind-mounts/
https://docs.docker.com/engine/reference/commandline/volume_create/

**networks**
https://docs.docker.com/engine/reference/commandline/network/
https://docs.docker.com/engine/reference/run/#network-settings
https://docs.docker.com/v17.09/engine/userguide/networking/#default-networks
https://docs.docker.com/v17.09/engine/userguide/networking/#the-default-bridge-network
https://docs.docker.com/v17.09/engine/userguide/networking/default_network/custom-docker0/
https://docs.docker.com/network/links/

**compose**
https://composerize.com/
https://docs.docker.com/compose/compose-file/
https://docs.docker.com/compose/reference/overview/

**stuff**
https://stackoverflow.com/questions/35594987/how-to-force-docker-for-a-clean-build-of-an-image
http://nginx.org/en/docs/http/ngx_http_upstream_module.html

**exit**
https://howchoo.com/g/zwjhogrkywe/how-to-add-a-health-check-to-your-docker-container
https://codeblog.dotsandbrackets.com/docker-health-check/
https://docs.docker.com/engine/swarm/

**anchor-engine**
https://github.com/anchore/anchore-engine
https://docs.anchore.com/current/docs/engine/engine_installation/docker_compose/
https://docs.anchore.com/current/docs/using/cli_usage/

errors:

https://github.com/anchore/anchore-cli/issues/7
