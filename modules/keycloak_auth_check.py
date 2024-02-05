import argparse
import sys

import requests
from argo_probe_keycloak.status import Status


def main():
    parser = argparse.ArgumentParser(
        description='Nagios probe for Keycloak login'
    )
    parser.add_argument(
        "--token_endpoint", dest="endpoint", type=str, required=True,
        help="The token endpoint"
    )
    parser.add_argument(
        "--client_id", dest="client_id", type=str, required=True,
        help="The identifier of the client"
    )
    parser.add_argument(
        "--client_secret", dest="client_secret", type=str, required=True,
        help="The secret value of the client"
    )
    parser.add_argument(
        "-t", "--timeout", dest="timeout", type=int, default=60,
        help="timeout"
    )
    args = parser.parse_args()

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

    print(status.get_message())
    sys.exit(status.get_code())


if __name__ == '__main__':
    main()
