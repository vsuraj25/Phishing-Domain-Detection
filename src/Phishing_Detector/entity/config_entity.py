from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    source_url : str
    local_data_dir_path : Path
    processed_data_dir_path : Path
    local_data_file_path : Path
    processed_data_file_path : Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    schema: dict
    processed_data_file_path: Path
    validation_report_dir_path : Path
    validation_report_file_path: Path
