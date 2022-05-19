import sys

from src.download import Downloader
from src.filters import WindowFilter
from src.train import TrainSender
from src.trigger import TriggerService


def download_scans_metadata():
    scans_downloader = Downloader()
    scans_metadata = scans_downloader.download_scans_metadata_from_s3()
    print(f'Finished Downloading ({len(scans_metadata)} scans)')
    return scans_metadata


def filter_by_windows(scans_metadata):
    window_filter = WindowFilter()
    valid_scans_metadata = [scan for scan in scans_metadata if window_filter.filter(scan)]
    print(f'Finished filtering good windows ({len(valid_scans_metadata)} valid scans)')
    return valid_scans_metadata


# noinspection PyShadowingNames
def trigger(trigger_service_api_key, valid_scans_metadata):
    trigger_service = TriggerService(trigger_service_api_key)
    trigger_results = {}
    for scan_metadata in valid_scans_metadata:
        scan_id = scan_metadata.series_instance_uid
        trigger_result = trigger_service.trigger_download(scan_id)
        if trigger_result is not None:
            trigger_results[scan_id] = trigger_result
    print(f'Finished triggering, {len(trigger_results)} successful triggers')
    return trigger_results


def train(trigger_results):
    trainer = TrainSender()
    successful = 0
    for scan_id, trigger_result in trigger_results.items():
        response = trainer.send_scan_to_train_queue(scan_id, trigger_result)
        if response is not None:
            successful += 1
    print(f'Finished training, {successful} successful triggers')


# noinspection PyShadowingNames
def main(trigger_service_api_key: str):
    scans_metadata = download_scans_metadata()

    valid_scans_metadata = filter_by_windows(scans_metadata)

    trigger_results = trigger(trigger_service_api_key, valid_scans_metadata)

    train(trigger_results)

    print('Mission Completed.')


if __name__ == '__main__':
    trigger_service_api_key = sys.argv[1]

    main(trigger_service_api_key)
