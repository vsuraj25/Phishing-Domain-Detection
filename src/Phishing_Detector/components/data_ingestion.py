import os
from Phishing_Detector.entity.config_entity import DataIngestionConfig
from Phishing_Detector.utils import *
from Phishing_Detector.constants import *
from scipy.io import arff
from urllib import request
import pandas as pd


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        logger.info(f"{'>'*10} Starting Data Ingestion Stage! {'<'*10}")
        logger.info(f"Getting Configuration for Data Ingestion Stage...")

        self.config = config
        logger.info(f"Configurations : {config}")

        logger.info(f"Creating required directories...")
        create_directories([config.local_data_dir_path])
        create_directories([config.processed_data_dir_path])

    def download_file(self):
        try:
            if not os.path.exists(self.config.local_data_file_path):
                logger.info(
                    f"Downloading source file from url{self.config.source_url} ..."
                )
                request.urlretrieve(
                    url=self.config.source_url,
                    filename=self.config.local_data_file_path,
                )
                logger.info(
                    f"File downloaded and saved to {self.config.local_data_file_path} ..."
                )
            else:
                logger.info(
                    f"File already present at path {self.config.local_data_file_path}"
                )
        except Exception as e:
            raise e

    def convert_to_csv(self):
        try:
            if not os.path.exists(self.config.processed_data_file_path):
                logger.info(f"Converting the downloaded arff file into csv format...")
                data = arff.loadarff(Path(self.config.local_data_file_path))
                data = pd.DataFrame(data[0])
                data = data.apply(lambda x: x.str.decode("utf8"))
                data = data.apply(pd.to_numeric, errors="ignore")
                data.to_csv(
                    path_or_buf=self.config.processed_data_file_path, index=False
                )
                logger.info(
                    f"File converted to csv and saved at {self.config.processed_data_file_path}"
                )
            else:
                logger.info(
                    f"File already present at path {self.config.processed_data_dir_path}"
                )

            logger.info(
                f"{'>'*10} Data Ingestion Stage Completed Successfully! {'<'*10}"
            )
        except Exception as e:
            raise e
