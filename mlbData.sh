#!/bin/bash
clear
date
docker rm mlb_data
docker rmi mlb_data
docker build -t mlb_data .
docker run --name mlb_test1 mlb_data
