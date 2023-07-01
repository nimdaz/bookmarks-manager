#!/bin/sh
docker build -t bookmarks-manager-dev .
docker rm bookmarks-manager-dev
docker run --name bookmarks-manager-dev bookmarks-manager-dev
