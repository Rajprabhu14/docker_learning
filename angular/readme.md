# create Angular project using docker

## Check any Folder available

ls -a
`docker pull trion/ng-cli`

## create angularApp

This command will create angular application in our localsystem
`docker run -u $(id -u) --rm -v "$PWD":/app trion/ng-cli ng new myapp`

## check any folder present in our system

`cd myapp`

## Test the development

`docker run -u $(id -u) --rm -p 4200:4200 -v "$PWD":/app trion/ng-cli ng serve --host 0.0.0.0 --disable-host-check`

## To check our app reflecting the changes

cd myapp/src/app/
vi app.component.ts

## Get the production built

cd && cd myapp
docker run -u $(id -u) --rm -v "$PWD":/app trion/ng-cli ng build

## To create the our ownimage

1. File Name should be Dockerfile
2. general practise for naming the our image is <docker_id>/<image_name>
3. Basic structure is docker build -t <name> <folder_location>
   eg. `docker build -t arulrajprabhu420/nginx .`
