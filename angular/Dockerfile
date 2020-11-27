# Base image
FROM nginx

LABEL maintainer="Demo LABEL"
# To install custom data
# RUN apt-get update && apt-get install -y net-tools && apt-get install -y procps
COPY /myapp/dist /usr/share/nginx/html
# add to image it can be used on process
ENV demo=daemon
COPY nginx.conf /etc/nginx/nginx.conf
# It will be added with CMD
ENTRYPOINT ["/docker-entrypoint.sh"]

# default running command
CMD ["nginx", "-g", "daemon off;"]