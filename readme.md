# Check docker installed

`docker -v`

# Run our first container

`docker run hello-world`

# Working with Docker

`docker run alpine ls -l`


`docker run alpine echo 'welcome'`

# Docker Help
`docker --help`

# List Images

`docker image ls`

# List container
## List all container  
  `docker ps -a`
## List running container
 `docker ps -a`

# container Management
## To Name our container
  `docker run --name mynginx nginx`
  
  docker run **--name mynginx** nginx
  
  To Stop the container press `ctrl+c`
## Start the stopped Container
   `docker start mynginx`
## Stop the running container
   `docker stop mynginx`
 
## Delete the Container
  `docker kill mynginx && docker rm mynginx`
## Delete container on kill
   `docker run --rm --name mynginx nginx`
   
   docker run **--rm** --name mynginx nginx
## Opening the port
  `docker run --name mynginx -d -p 80:80 nginx`
  
  docker run --name mynginx -d  **-p <sytem_port>:<container_port>** nginx
 
 
# Linux command Used

| command                                                     | usage                                                     |
| ---------------------------------------------------------- | -------------------------------------------------------- |
| ls                               |list file                                        |
| ps                                    | running process |
| kill |   Stop the running process      |
| rm |  Remove the given item      |
| && |  Run the second command if first succed     |
| -d |  daemon process or Run the process in background      |
