import json
from pathlib import Path

import pytest

from src.filters import WindowFilter, Range
from src.scans import ScanMetadata

SAMPLE_PATH = Path('../resources/tests/scan_metadata_1.json')


@pytest.fixture
def scan_metadata_sample() -> ScanMetadata:
    sample: ScanMetadata = ScanMetadata.from_json(SAMPLE_PATH.read_text())
    sample.window_center = 250
    sample.window_width = 250
    return sample


@pytest.fixture
def tested_window_filter() -> WindowFilter:
    return WindowFilter(window_center_range=Range(100, 200), window_width_range=Range(300, 400))


# noinspection PyShadowingNames
def test_width_filter_both_out_of_scope(scan_metadata_sample: ScanMetadata, tested_window_filter: WindowFilter):
    assert tested_window_filter.filter(scan_metadata_sample) is False


# noinspection PyShadowingNames
def test_width_filter_center_out_of_scope(scan_metadata_sample: ScanMetadata, tested_window_filter: WindowFilter):
    scan_metadata_sample.window_width = 350
    assert tested_window_filter.filter(scan_metadata_sample) is False


# noinspection PyShadowingNames
def test_width_filter_width_out_of_scope(scan_metadata_sample: ScanMetadata, tested_window_filter: WindowFilter):
    scan_metadata_sample.window_center = 150
    assert tested_window_filter.filter(scan_metadata_sample) is False


# noinspection PyShadowingNames
def test_width_filter_within_scope(scan_metadata_sample: ScanMetadata, tested_window_filter: WindowFilter):
    scan_metadata_sample.window_center = 150
    scan_metadata_sample.window_width = 350
    assert tested_window_filter.filter(scan_metadata_sample) is True
