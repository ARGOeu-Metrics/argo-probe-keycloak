import requests
from argo_probe_keycloak.status import Status


def fetch_keycloak_token(args):
    status = Status()

    try:
        response = requests.post(
            args.endpoint,
            auth=(args.client_id, args.client_secret),
            data={
                "client_id": args.client_id,
                "client_secret": args.client_secret,
                "grant_type": "client_credentials"
            },
            timeout=args.timeout
        )
        response.raise_for_status()

        access_token = response.json()["access_token"]
        assert access_token

        status.set_ok("Access token fetched successfully.")

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
        ValueError,
        KeyError,
        AssertionError
    ) as e:
        status.set_critical(str(e))

    return {
        "message": status.get_message(),
        "code": status.get_code()
    }
