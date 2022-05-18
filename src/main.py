import json
from collections import defaultdict, Counter

from src.data import ScanMetadata
from src.download import download_scans_metadata_from_s3
from src.filters import WindowFilter


def cache_scans_locally():
    scans = download_scans_metadata_from_s3()

    with open('../resources/all_scans.json', 'w') as f:
        f.write(json.dumps([scan.to_dict() for scan in scans]))
    print('downloaded all scans')


def count_window_values_per_series_instance_uid(scans):
    series = defaultdict(set)
    for scan in scans:
        series[scan.series_instance_uid].add((scan.window_center, scan.window_width))
    for series_uid, params in series.items():
        print(f'{series_uid}: {Counter(params)}')


def load_scans_cache():
    return [ScanMetadata.from_dict(scan_dict) for scan_dict in json.loads(open('../resources/all_scans.json').read())]


def count_stuff(scans):
    series_instance_count = json.dumps(dict(Counter((scan.series_instance_uid for scan in scans))), indent=2)
    print(series_instance_count)
    print()

    series = defaultdict(list)
    for scan in scans:
        series[scan.series_instance_uid].append(scan)
    unique_instances = {uid: len(set((s.instance_number for s in scans))) for uid, scans in series.items()}
    print(json.dumps(unique_instances, indent=2))

    print(series_instance_count == unique_instances)

    window_filter = WindowFilter()
    valid_windows = {uid: len([s for s in scans if window_filter.filter(s)]) for uid, scans in series.items()}
    series_valid_percentages = {series_uid: valid_windows[series_uid] / unique_instances[series_uid] for series_uid in valid_windows}
    print(json.dumps(series_valid_percentages, indent=2))


if __name__ == '__main__':
    all_scans = load_scans_cache()
    count_stuff(all_scans)

