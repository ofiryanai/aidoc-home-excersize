from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ScanMetadata:
    series_instance_uid: str
    instance_number: int
    window_center: float
    window_width: float
