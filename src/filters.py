from abc import abstractmethod
from dataclasses import dataclass

from src.scans import ScanMetadata


class ScanFilter:

    @abstractmethod
    def filter(self, scan_metadata: ScanMetadata):
        pass


@dataclass
class Range:
    low: float
    high: float

    def __contains__(self, item: float):
        return self.low < item < self.high


class WindowFilter(ScanFilter):
    DEFAULT_CENTER_RANGE = Range(150, 300)
    DEFAULT_WIDTH_RANGE = Range(450, 600)

    def __init__(self,
                 window_center_range: Range = DEFAULT_CENTER_RANGE,
                 window_width_range: Range = DEFAULT_WIDTH_RANGE):
        self.window_center_range = window_center_range
        self.window_width_range = window_width_range

    def filter(self, scan_metadata: ScanMetadata):
        center_within_range = scan_metadata.window_center in self.window_center_range
        width_within_range = scan_metadata.window_width in self.window_width_range
        return center_within_range and width_within_range

    def __repr__(self):
        return f'WindowFilter(center_range={self.window_center_range}, width_range={self.window_width_range})'
