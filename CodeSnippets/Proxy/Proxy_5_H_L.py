# Proxy Service class that handles requests on behalf of the Real Service object
class ProxyService:
    def __init__(self, service_url):
        self.service_url = service_url

    # Proxy method that makes a GET request to the Real Service API
    def get(self, path):
        response = requests.get(f"{self.service_url}{path}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to retrieve data from Real Service API")