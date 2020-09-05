from jfahrer/nginx:latest

RUN apt-get update && apt-get install gettext-base

ENV PROXY_PROTOCOL=http PROXY_UPSTREAM=example.com

copy proxy.conf /etc/nginx/sites-available/default.template

copy start.sh /
CMD ["/start.sh"]
# docker container run --rm --network demo -p 81:80 --name demo-lb -e PROXY_UPSTREAM=webapp:9292  demo/lb:latest
# docker container run -d --rm --name pg --network demo -e "POSTGRES_USER=web_app" -e "POSTGRES_PASSWORD=secret" -e "POSTGRES_DB=web_app_db" -p 9292:9292 postgres
# docker container run --rm  --network demo --name webapp -e POSTGRES_PASSWORD=secret jfahrer/demo_web_app

# docker container run --rm --network demo --env-file db.env --name pg -d postgres
# docker container run --rm  -d --network demo --env-file app.env jfahrer/demo_web_app

# last working example
# docker container run --rm --name pg --network demo --env-file db.env -d postgres:alpine
# docker container run --rm -d --network demo --net-alias=webapp --env-file app.env jfahrer/demo_web_app
# docker container run --rm --name lb --network demo -p 81:80 -e PROXY_UPSTREAM='webapp:9292' -d jfahrer/lb:latest