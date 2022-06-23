#!/bin/bash

curl -X POST http://localhost:5000/api/timeline_post -d 'name=Mustafa Abdulrahman&email=mus2003.abdul@gmail.com&content=Adding Database part 2'

ID=$(curl http://localhost:5000/api/timeline_post | jq '.timeline_posts[0].id')

curl http://localhost:5000/api/timeline_post

curl -X DELETE "http://localhost:5000/api/timeline_post/${ID}"

curl http://localhost:5000/api/timeline_post

