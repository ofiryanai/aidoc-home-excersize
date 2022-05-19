from http import HTTPStatus

import requests

from src.data import ScanTriggerResult

SERVICE_URL = 'https://3tr13vrmf7.execute-api.eu-west-2.amazonaws.com/v1/scan-fetcher'


class TriggerService:
    def __init__(self, api_key: str, service_url: str = SERVICE_URL):
        self.service_url = service_url
        self.api_key = api_key

    def trigger_download(self, scan_series_instance_uid: str):
        payload = {'series_instance_uid': scan_series_instance_uid}
        try:
            response = requests.post(self.service_url,
                                     json=payload,
                                     headers={'x-api-key': self.api_key})
            if response.status_code != HTTPStatus.OK:
                raise RuntimeError(f'Bad status code: {response.status_code}')
        except (requests.RequestException, RuntimeError) as e:
            print(f'ERROR Failed triggering download for {scan_series_instance_uid} due to {repr(e)}')
            return None

        response_payload = response.json()
        trigger_result = ScanTriggerResult.from_dict(response_payload)
        return trigger_result
