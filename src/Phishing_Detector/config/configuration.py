from Phishing_Detector.utils import *
from Phishing_Detector.constants import *
from Phishing_Detector import logger
from Phishing_Detector.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainingConfig,
    ModelEvaluationConfig,
)


class ConfigurationManager:
    def __init__(self, config_path=CONFIG_FILE_PATH, params_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_dir_path=config.local_data_dir_path,
            processed_data_dir_path=config.processed_data_dir_path,
            local_data_file_path=config.local_data_file_path,
            processed_data_file_path=config.processed_data_file_path,
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            schema=config.schema,
            processed_data_file_path=config.processed_data_file_path,
            validation_report_dir_path=config.validation_report_dir_path,
            validation_report_file_path=config.validation_report_file_path,
        )

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        params = self.params
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_validation_report=config.data_validation_report,
            processed_data_file_path=config.processed_data_file_path,
            transformed_data_dir_path=config.transformed_data_dir_path,
            transformed_data_file_path=config.transformed_data_file_path,
            train_test_data_dir_path=config.train_test_data_dir_path,
            x_train_file_path=config.x_train_file_path,
            x_test_file_path=config.x_test_file_path,
            y_train_file_path=config.y_train_file_path,
            y_test_file_path=config.y_test_file_path,
            param_imputer_strategy=params.IMPUTER_STRATEGY,
            param_test_size=params.TEST_SIZE,
            param_random_state=params.RANDOM_STATE,
            param_target=params.TARGET,
            param_cols_drop= params.COLS_TO_DROP
        )

        return data_transformation_config

    def get_model_training_config(self) -> ModelTrainingConfig:
        config = self.config.model_training
        params = self.params
        create_directories([config.root_dir])

        model_training_config = ModelTrainingConfig(
            root_dir=config.root_dir,
            x_train_file_path=config.x_train_file_path,
            y_train_file_path=config.y_train_file_path,
            saved_model_dir_path=config.saved_model_dir_path,
            saved_model_file_path=config.saved_model_file_path,
            param_hidden_layer_sizes=params.hidden_layer_sizes,
            param_max_iter=params.max_iter,
            param_activation=params.activation,
            param_solver=params.solver,
        )

        return model_training_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params
        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            x_test_file_path=config.x_test_file_path,
            y_test_file_path=config.y_test_file_path,
            saved_model_file_path=config.saved_model_file_path,
            model_metrics_dir_path=config.model_metrics_dir_path,
            model_metrics_json_file_path=config.model_metrics_json_file_path,
            model_metrics_cmat_file_path=config.model_metrics_cmat_file_path,
            param_hidden_layer_sizes=params.hidden_layer_sizes,
            param_max_iter=params.max_iter,
            param_activation=params.activation,
            param_solver=params.solver,
            param_reg_model_name=params.registered_model_name,
        )

        return model_evaluation_config
