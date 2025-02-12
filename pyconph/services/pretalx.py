import requests

class PretalxService:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
                }

    def get_event(self, event_slug: str):
        url = f"{self.base_url}/api/events/{event_slug}/"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.ok else response.raise_for_status()

    def get_submissions(self, event_slug: str):
        url = f"{self.base_url}/api/events/{event_slug}/submissions/"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.ok else response.raise_for_status()

    def get_speakers(self, event_slug: str):
        url = f"{self.base_url}/api/events/{event_slug}/speakers/"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.ok else response.raise_for_status()

    def get_talks(self, event_slug: str):
        url = f"{self.base_url}/api/events/{event_slug}/talks?limit=999&state=confirmed"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.ok else response.raise_for_status()

    def update_submission(self, event_slug: str, submission_id: str, data: dict):
        response = requests.patch(url, json=data, headers=self.headers)
        return response.json() if response.ok else response.raise_for_status()

    def send_feedback(self, event_slug: str, submission_id: str, feedback: dict):
        url = f"{self.base_url}/api/events/{event_slug}/submissions/{submission_id}/feedback/"
        response = requests.post(url, json=feedback, headers=self.headers)
        return response.json() if response.ok else response.raise_for_status()
