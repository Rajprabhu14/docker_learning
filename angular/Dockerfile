# Base image
FROM nginx

LABEL maintainer="Demo LABEL"
# To install custom data
# RUN apt-get update && apt-get install -y net-tools && apt-get install -y procps
COPY /myapp/dist /usr/share/nginx/html

# It will be added with CMD
ENTRYPOINT ["/docker-entrypoint.sh"]

# default running command
CMD ["nginx", "-g", "daemon off;"]