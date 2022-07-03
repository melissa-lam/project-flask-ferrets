#!/bin/bash

#POST command should be like the following:
#curl --request POST http://localhost:5000/api/timeline_post -d 
# 'name=Melissa&email=melissa21lam@gmail.com&content=Just Added Database to my portfolio site!'
#run by ./curl-test.sh 'name=Melissa&email=melissa21lam@gmail.com&content=Just Added Database to my portfolio site!'

curl --request POST http://localhost:5000/api/timeline_post -d "name=$1&email=$2&content=${*:3}"

curl http://localhost:5000/api/timeline_post
