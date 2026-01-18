import requests

def get_metrics(endpoint, interval):
    url = endpoint
    if interval:
        url += f"?interval={interval}"

    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception()
    
    return response.json()

def iter_metrics(endpoint, interval):
    while True:
        yield get_metrics(endpoint, interval)
        
        
class SyncHttpGetMetricsCollector:
    def __init__(self, endpoint, interval):
        self.url = endpoint
        if interval:
            self.url += f"?interval={interval}"
            
        self.interval = interval
        
    def get(self):
        response = requests.get(self.url)
        
        if response.status_code != 200:
            raise Exception(f"Respons status code was not {response.status_code}")
        
        return response.json()
    
    def __iter__(self):
        while True:
            yield self.get()
