#!/bin/bash

docker buildx build \
  --platform linux/amd64 \
  -f Dockerfile.latexmk \
  -t "ghcr.io/vitomakarevich/python312-latexmk:4" \
  .

echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin

docker push "ghcr.io/vitomakarevich/python312-latexmk:4"