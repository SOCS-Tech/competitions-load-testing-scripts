def get_bearer_token(client, auth_host, timeout_duration):
    """
    Fetch the bearer token before starting the test.
    """

    payload = {
        "grant_type": "client_credentials",
        "client_id": "GPS_LAYERCAKE",
        "client_secret": "y'rNbU2;c8DvqH}EBw0Z]Hp+(|}{f.gI",
        "scope": "Competition"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    with client.post(
        url=f"{auth_host}/connect/token",
        data=payload,
        headers=headers,
        name="Get Bearer Token",
        catch_response=True,
        timeout=timeout_duration
    ) as response:
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            return None