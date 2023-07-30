import requests

class PrometheusClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def query(self, query):
        response = requests.get(f"{self.base_url}/api/v1/query", params={"query": query})
        # handle response, convert to desired format, handle errors, etc.
        return data
