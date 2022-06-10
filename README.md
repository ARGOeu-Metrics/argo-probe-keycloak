# argo-probe-keycloak

Probe is obtaining an access token from client id and secret value.

## Synopsis

The `check-keycloak` probe has four arguments. In order to obtain the access token, one must provide token endpoint from which to fetch the token, client ID and client secret. If the token has been successfully fetched, the probe returns OK status.

```
# /usr/libexec/argo/probes/keycloak/check-keycloak --help
usage: check-keycloak [-h] --token_endpoint ENDPOINT --client_id CLIENT_ID
                      --client_secret CLIENT_SECRET [-t TIMEOUT]

Nagios probe for Keycloak login

optional arguments:
  -h, --help            show this help message and exit
  --token_endpoint ENDPOINT
                        The token endpoint
  --client_id CLIENT_ID
                        The identifier of the client
  --client_secret CLIENT_SECRET
                        The secret value of the client
  -t TIMEOUT, --timeout TIMEOUT
                        timeout
```

Example execution of the probe:

```
# /usr/libexec/argo/probes/keycloak/check-keycloak -t 60 --client_id <client_id> --client_secret <client_secret> --token_endpoint  https://sso.neanias.eu/auth/realms/neanias-development/protocol/openid-connect/token
OK - Access token fetched successfully.
```
