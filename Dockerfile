## Base image
FROM python:3.8.5-alpine3.11

## install git for downloading the file
# RUN apk update && apk upgrade && \
#     apk add --no-cache bash git openssh
# RUN git clone https://ktalk.kcubeconsulting.com/docker_demo/scrapping.git


## copy required files
RUN mkdir -p scrapping
copy rentfa.py /scrapping


copy requirements.txt /scrapping
## Make Sure the data directory present
RUN mkdir -p data
ENV LOCAL_DATA_LOCATION='/data'

## clone the data from git
## install required packages
WORKDIR "scrapping"
RUN pip install -r requirements.txt
## start when run the image for container
# CMD ['/data']
# ENTRYPOINT [ "python",  "rentfa.py" ]
ENTRYPOINT [ "sh" ]

