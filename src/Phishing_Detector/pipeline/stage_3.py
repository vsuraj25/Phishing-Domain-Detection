from Phishing_Detector.components import DataTransformation
from Phishing_Detector.config import ConfigurationManager


def main():
    config = ConfigurationManager()
    data_transformation_config = config.get_data_transformation_config()
    data_transformation = DataTransformation(config=data_transformation_config)
    data_transformation.transform_data()
    data_transformation.split_data()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
