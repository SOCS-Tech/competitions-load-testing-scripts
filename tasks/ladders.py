import os
import logging

def get_ladders(client, token, host, timeout_duration, DEBUG_MODE):
    """
    Perform a GET request to fetch ladders.
    """
    if not token:
        logging.error("Bearer token is missing. Skipping request.")
        return

    url = f"{host}/api/ladders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # Add body with Compeitition ID
    body = {
        "competitionId": "84aa37d1-541d-03d9-1986-3a197924ccca"
    }

    with client.get(
        url=url,
        headers=headers,
        params=body,
        name="Get Ladders",
        catch_response=True,
        timeout=timeout_duration
    ) as response:
        if response.status_code == 200:
            response.success()
            if DEBUG_MODE:
                logging.info(f"GET {url} succeeded with response: {response.text}")
        elif response.status_code == 429:
            response.success("Rate limit hit and 429 code received")
            if DEBUG_MODE:
                logging.warning(f"Rate limit hit: {response.text}")
        else:
            response.failure(f"GET {url} failed with status {response.status_code}")
            if DEBUG_MODE:
                logging.error(f"Request URL: {url}, Headers: {headers}, Response: {response.text}")