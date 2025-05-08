import os
import logging
from locust import HttpUser, task, between
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ApiUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.socscompetition.com/api/competitions"
    auth_host = "https://auth.socscompetition.com"
    timeout_duration = 90
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'True') == 'True'
    token = None

    def on_start(self):
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

        with self.client.post(
            url=f"{self.auth_host}/connect/token",
            data=payload,
            headers=headers,
            name="Get Bearer Token",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                if self.DEBUG_MODE:
                    logging.info("Successfully retrieved bearer token.")
            else:
                response.failure("Failed to retrieve bearer token.")
                if self.DEBUG_MODE:
                    logging.error(f"Auth response: {response.text}")

    @task
    def run_scenario(self):
        # Step 1: GET request to the base URL
        self.get_competitions()

    def get_competitions(self):
        """
        Perform a GET request to fetch competitions.
        """
        if not self.token:
            logging.error("Bearer token is missing. Skipping request.")
            return

        url = f"{self.host}/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        with self.client.get(
            url=url,
            headers=headers,
            name="Get Competitions",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                response.success()
                if self.DEBUG_MODE:
                    logging.info(f"GET {url} succeeded with response: {response.text}")
            if response.status_code == 429:
                response.success("Rate limit hit and 429 code received")
                if self.DEBUG_MODE:
                    logging.warning(f"Rate limit hit: {response.text}")
            else:
                response.failure(f"GET {url} failed with status {response.status_code}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Headers: {headers}, Response: {response.text}")

    def on_stop(self):
        """
        Clean up any resources created during the test.
        """
        if self.DEBUG_MODE:
            logging.info("Test completed. No resources to clean up.")