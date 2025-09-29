#!/bin/bash

docker buildx build \
  --platform linux/amd64 \
  -f Dockerfile \
  -t "ghcr.io/vitomakarevich/cv-tuner:latest" \
  .

echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin

docker push "ghcr.io/vitomakarevich/cv-tuner:latest"