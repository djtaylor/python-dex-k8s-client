#!/bin/bash

OIDC_CLIENT_ID="$(docker logs hydra-oidc-server 2>&1 | \
  grep client_id | \
  jq .msg | \
  sed 's/^\"client_id: \(.*\)\"$/\1/g')"
OIDC_CLIENT_SECRET="$(docker logs hydra-oidc-server 2>&1 | \
  grep client_secret | \
  jq .msg | \
  sed 's/^\"client_secret: \(.*\)\"$/\1/g')"

echo -e "#!/bin/bash\nexport OIDC_CLIENT_ID='${OIDC_CLIENT_ID}'\n\
export OIDC_CLIENT_SECRET='${OIDC_CLIENT_SECRET}'\n" > .oidc_client
