import requests
from argo_probe_keycloak.status import Status


def fetch_keycloak_token(endpoint, client_id, client_secret, timeout):
    status = Status()

    try:
        response = requests.post(
            endpoint,
            auth=(client_id, client_secret),
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials"
            },
            timeout=timeout
        )
        response.raise_for_status()

        access_token = response.json()["access_token"]
        assert access_token

        status.set_ok("Access token fetched successfully.")

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException
    ) as e:
        status.set_critical(str(e))

    except AssertionError:
        status.set_critical(
            "Access token not fetched - not defined in response json"
        )

    except KeyError:
        status.set_critical(
            "Access token not fetched - key 'access_token' not defined in "
            "response json"
        )

    return {
        "message": status.get_message(),
        "code": status.get_code()
    }
