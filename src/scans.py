from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ScanMetadata:
    series_instance_uid: str
    instance_number: int
    window_center: float
    window_width: float


@dataclass_json
@dataclass
class ScanTriggerResult:
    accession_number: int
    series_number: int
    spacing_between_slices: int
    slice_thickness: float
    window_center: float
    window_width: float
    patient_position: str
    hospital_id: str
    report_exists: bool

