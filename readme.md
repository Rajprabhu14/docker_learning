# Build the image

`docker build -t rentscraping:latest .`

# create volume

`docker container run -it --name demo -v data rentscraping:latest`

# To start detach volume

`docker container start demo`

# To debug the existing container

`docker container exec -it demo bash`

# To bind the local folder to volume

`docker container run --name demo --mount type=bind,src=/k/docker_demo_volume,dst=/data rentscraping:latest`

# Difference between mount & volume

| Volume                                                     | Bind                                                     |
| ---------------------------------------------------------- | -------------------------------------------------------- |
| managed via Docker client                                  | we need to handle                                        |
| Independent file system                                    | The container has access to the files on the docker host |
| **usage**: backup & configuration(share between container) | **usage**: handling sourcode, configuration file         |
