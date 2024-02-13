import requests
from argo_probe_keycloak.status import Status


def fetch_keycloak_token(endpoint, client_id, client_secret, timeout):
    status = Status()

    perfdata = ""
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
        perfdata = (f"|time={response.elapsed.total_seconds()}s;"
                    f"size={len(response.content)}B")

        response.raise_for_status()

        access_token = response.json()["access_token"]
        assert access_token

        status.set_ok(f"Access token fetched successfully{perfdata}")

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException
    ) as e:
        status.set_critical(f"{str(e)}{perfdata}")

    except AssertionError:
        status.set_critical(
            f"Access token not fetched - not defined in response json{perfdata}"
        )

    except KeyError:
        status.set_critical(
            f"Access token not fetched - key 'access_token' not defined in "
            f"response json{perfdata}"
        )

    return {
        "message": status.get_message(),
        "code": status.get_code()
    }
