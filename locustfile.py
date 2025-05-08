import os
import logging
from locust import HttpUser, task, between
from dotenv import load_dotenv
from utils.token_utils import get_bearer_token
from tasks.competitions import get_competitions

# Load environment variables
load_dotenv()

class CompetitionsUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.socscompetition.com/api/competitions"
    auth_host = "https://auth.socscompetition.com"
    timeout_duration = 90
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'True') == 'True'
    token = None

    def on_start(self):
        token = get_bearer_token(self.client, self.auth_host, self.timeout_duration)

        if token:
            self.token = token
            if self.DEBUG_MODE:
                logging.info("Successfully retrieved bearer token.")
        else:
            logging.error("Failed to retrieve bearer token.")
            raise Exception("Bearer token retrieval failed.")

    @task
    def run_scenarios(self):
        get_competitions(
            client=self.client,
            token=self.token,
            host=self.host,
            timeout_duration=self.timeout_duration,
            DEBUG_MODE=self.DEBUG_MODE
        )

    def on_stop(self):
        """
        Clean up any resources created during the test.
        """
        if self.DEBUG_MODE:
            logging.info("Test completed. No resources to clean up.")