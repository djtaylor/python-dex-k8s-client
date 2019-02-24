#!/bin/bash
source .oidc_client
source docker-compose.env

docker exec -it hydra-oidc-server hydra $@ \
--id ${OIDC_CLIENT_ID} \
--secret ${OIDC_CLIENT_SECRET} \
--url https://localhost:4444
