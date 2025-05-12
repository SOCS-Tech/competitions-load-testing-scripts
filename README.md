# competitions-load-testing-scripts


This repository contains Locust-based load testing scripts for the SOCS Competitions External API.

## ✅ Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Locust](https://docs.locust.io/en/stable/installation.html):
  ```bash
  pip install locust
- Ensure locust is added to Enviroment variables by adding the Python Scripts directory to the PATH enviroment variable, located in System variables.

## ✅ Running Project
- Open a terminal and use the command locust to startup the locustfile.py file
- This will open a local server on http://localhost:8089.
- Read me at: [Azure Load Testing](https://marketplace.visualstudio.com/items?itemName=ms-azure-load-testing.microsoft-testing)

## ✅ Uploading to Azure Load Tester
- Ensure locust.py is uploaded and set as the main test script file
- Requirements.txt also needs uploading to add required libraries
- If a folder needs uploading,  for example tasks or utils, each folder will need to be zipped on it's own and uploaded