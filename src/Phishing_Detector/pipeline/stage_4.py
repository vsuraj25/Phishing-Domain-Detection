from Phishing_Detector.components import ModelTraining
from Phishing_Detector.config import ConfigurationManager


def main():
    config = ConfigurationManager()
    model_training_config = config.get_model_training_config()
    model_trainer = ModelTraining(config = model_training_config)
    model_trainer.train_model()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e
