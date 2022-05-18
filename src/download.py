from traceback import print_exc
from typing import List

from cloudpathlib import CloudPath, S3Path

from src.data import ScanMetadata

SCANS_S3_URI = 's3://aidoc-data-eng-interviews/scans-metadata/'


def download_scans_metadata_from_s3(s3_uri: str = SCANS_S3_URI) -> List[ScanMetadata]:
    scans_metadata = []

    scans_metadata_s3_path: S3Path
    for scans_metadata_s3_path in CloudPath(s3_uri).glob('*'):
        print(scans_metadata_s3_path)
        scans_metadata_bulk: str = scans_metadata_s3_path.read_text()
        for raw_scan_metadata in scans_metadata_bulk.splitlines():
            try:
                scan_metadata = ScanMetadata.from_json(raw_scan_metadata)
                scans_metadata.append(scan_metadata)
            except Exception:
                print_exc()
                print(f'ERROR Malformed scan: {raw_scan_metadata}')
        print(len(scans_metadata))

    return scans_metadata
