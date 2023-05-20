from Phishing_Detector.entity.config_entity import DataTransformationConfig
from Phishing_Detector.utils import *
from Phishing_Detector.constants import *
from Phishing_Detector import logger
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import pandas as pd


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        logger.info(f"{'>'*10} Starting Data Transformation Stage! {'<'*10}")

        logger.info(f"Getting Configuration for Data Transformation Stage...")
        self.config = config
        logger.info(f"Configurations : {config}")

        logger.info(f"Creating required directories...")
        create_directories([self.config.transformed_data_dir_path])
        create_directories([self.config.train_test_data_dir_path])

    def get_validation_status(self) -> bool:
        try:
            logger.info(f"Loading data validation report...")
            validation_report = load_json(Path(self.config.data_validation_report))
            final_validation_status = validation_report["final_validation_status"]
            logger.info(f"Data Validation Status : {final_validation_status}")
            return final_validation_status
        except Exception as e:
            raise e

    def transform_data(self):
        try:
            if self.get_validation_status():
                logger.info(f"Reading the validated data...")
                data = pd.read_csv(self.config.processed_data_file_path)

                logger.info(
                    f"Filling null values using SimpleImputer(strategy = {self.config.param_imputer_strategy})..."
                )
                imputer = SimpleImputer(strategy=self.config.param_imputer_strategy)
                imputer.fit(data)
                logger.info(f"Null Values Imputed Successfully...")
                imputed_data = imputer.transform(data)
                imputed_df = pd.DataFrame(imputed_data, columns=data.columns)
                imputed_df.to_csv(self.config.transformed_data_file_path, index=False)
                logger.info(
                    f"Transformed Data Saved at {self.config.transformed_data_file_path}..."
                )
            else:
                logger.info(
                    f"Data is not validated - Validation Status = {self.get_validation_status()}"
                )
        except Exception as e:
            raise e

    def split_data(self):
        try:
            logger.info(f"Splitting the transformed data into train and test splits...")

            data = pd.read_csv(self.config.transformed_data_file_path)
            X = data.drop(self.config.param_target, axis=1)
            Y = data[self.config.param_target]
            x_train, x_test, y_train, y_test = train_test_split(
                X,
                Y,
                test_size=self.config.param_test_size,
                random_state=self.config.param_random_state,
            )
            logger.info(f"Train and test splits created successfully...")

            x_train.to_csv(self.config.x_train_file_path, index=False)
            logger.info(f"x_train saved at {self.config.x_train_file_path}")

            x_test.to_csv(self.config.x_test_file_path, index=False)
            logger.info(f"x_test saved at {self.config.x_test_file_path}")

            y_train.to_csv(self.config.y_train_file_path, index=False)
            logger.info(f"y_train saved at {self.config.y_train_file_path}")

            y_test.to_csv(self.config.y_test_file_path, index=False)
            logger.info(f"y_test saved at {self.config.y_test_file_path}")

            logger.info(
                f"{'>'*10} Data Transformation Stage Completed Successfully! {'<'*10}"
            )

        except Exception as e:
            raise e
