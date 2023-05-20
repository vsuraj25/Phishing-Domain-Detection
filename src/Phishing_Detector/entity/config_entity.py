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

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_validation_report: Path
    processed_data_file_path: Path
    transformed_data_dir_path: Path
    transformed_data_file_path: Path
    train_test_data_dir_path: Path
    x_train_file_path: Path
    x_test_file_path: Path
    y_train_file_path: Path
    y_test_file_path: Path
    param_imputer_strategy: str
    param_test_size: float
    param_random_state: int
    param_target: str

@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir : Path
    x_train_file_path : Path
    y_train_file_path : Path
    saved_model_dir_path : Path
    saved_model_file_path : Path
    param_hidden_layer_sizes: tuple
    param_max_iter: int
    param_activation: str
    param_solver: str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir : Path
    x_test_file_path : Path
    y_test_file_path : Path
    saved_model_file_path : Path
    model_metrics_dir_path : Path
    model_metrics_json_file_path : Path
    model_metrics_cmat_file_path : Path
