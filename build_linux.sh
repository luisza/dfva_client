#!/bin/sh

VERSION=$(awk '{print $3}' src/client_fva/__init__.py)
VERSION=echo "${VERSION//\'//}" 
NAME='client_fva'
PACKAGE='clientfva'
ARCH='amd64'

docker build -q -t debbuilder -f builder/Dockerfile_Debian .
docker build -q -t rpmbuilder -f builder/Dockerfile_Fedora .
docker build -q -t rpmbuildercentos -f builder/Dockerfile_Centos .
mkdir -p rpm
mkdir -p deb
mkdir -p release

chmod 777 rpm
chmod 777 deb

docker run --env VERSION=$VERSION --env NAME=$NAME --env ARCH=$ARCH  --env OS='centos' -v $(pwd)/rpm:/packages rpmbuildercentos
docker run --env VERSION=$VERSION --env NAME=$NAME --env ARCH=$ARCH  --env OS='fedora' -v $(pwd)/rpm:/packages rmpbuilder
docker run --env VERSION=$VERSION --env NAME=$NAME --env ARCH=$ARCH --env PACKAGE=$PACKAGE -v $(pwd)/deb:/packages debbuilder

cp rpm/* release/
cp deb/* release/
