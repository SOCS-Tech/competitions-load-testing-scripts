import os
import logging

def get_seasons(client, token, host, timeout_duration, DEBUG_MODE):
    """
    Perform a GET request to fetch seasons.
    """
    if not token:
        logging.error("Bearer token is missing. Skipping request.")
        return

    url = f"{host}/api/seasons"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    with client.get(
        url=url,
        headers=headers,
        name="Get Seasons",
        catch_response=True,
        timeout=timeout_duration
    ) as response:
        if response.status_code == 200:
            response.success()
            if DEBUG_MODE:
                logging.info(f"GET {url} succeeded with response: {response.text}")
        elif response.status_code == 429:
            response.success()
            if DEBUG_MODE:
                logging.warning(f"Rate limit hit: {response.text}")
        else:
            response.failure(f"GET {url} failed with status {response.status_code}")
            if DEBUG_MODE:
                logging.error(f"Request URL: {url}, Headers: {headers}, Response: {response.text}")