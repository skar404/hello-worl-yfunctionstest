#!/usr/bin/env bash

zip -r app.zip * --exclude "*.log" --exclude "*venv*" --exclude "deploy.sh"

yc serverless function version create \
  --function-name=test \
  --runtime python37 \
  --entrypoint main.handler \
  --memory 128m \
  --execution-timeout 5s \
  --source-path ./app.zip

rm app.zip
