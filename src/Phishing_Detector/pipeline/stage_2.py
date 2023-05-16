from Phishing_Detector.components import DataValidation
from Phishing_Detector.config import ConfigurationManager


def main():
    config = ConfigurationManager()
    data_validation_config = config.get_data_validation_config()
    data_validation = DataValidation(config = data_validation_config)
    data_validation.validate_data()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e
