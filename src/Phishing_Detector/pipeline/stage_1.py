from Phishing_Detector.components import DataIngestion
from Phishing_Detector.config import ConfigurationManager
from Phishing_Detector import logger


def main():
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.convert_to_csv()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
