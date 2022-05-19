import base64

import boto3
from botocore.exceptions import ClientError

from src.data import ScanTriggerResult

sqs_client = boto3.client('sqs', region_name='eu-west-2')

QUEUE_NAME = 'aidoc-pandemic-algo-trainer-ofir'


class TrainSender:
    def __init__(self, queue_name=QUEUE_NAME):
        try:
            self.queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
        except (ClientError, KeyError) as e:
            print(f'ERROR Failed to get queue url due to {repr(e)}')

    def send_scan_to_train_queue(self, scan_series_instance_uid: str, scan_trigger_result: ScanTriggerResult):
        message_payload = self._serialize_trigger_result(scan_trigger_result)
        try:
            response = sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_payload
            )
            response_status = response['ResponseMetadata']['HTTPStatusCode']
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise RuntimeError(f'Bad response status: {response_status}')
            return response
        except (ClientError, RuntimeError) as e:
            print(f'ERROR Failed to send train task for {scan_series_instance_uid} due to {repr(e)}')

    @staticmethod
    def _serialize_trigger_result(trigger_result: ScanTriggerResult) -> str:
        result_json = trigger_result.to_json()
        result_json_bytes = result_json.encode()
        result_base64 = base64.b64encode(result_json_bytes)
        return result_base64.decode()
