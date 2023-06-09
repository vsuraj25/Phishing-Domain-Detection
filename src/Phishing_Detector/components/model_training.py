from Phishing_Detector.entity.config_entity import ModelTrainingConfig
from Phishing_Detector.utils import *
from Phishing_Detector.constants import *
from Phishing_Detector import logger
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib


class ModelTraining:
    def __init__(self, config: ModelTrainingConfig):
        logger.info(f"{'>'*10} Starting Model Training Stage! {'<'*10}")

        logger.info(f"Getting Configuration for Model Training Stage...")
        self.config = config
        logger.info(f"Configurations : {config}")

        logger.info(f"Creating required directories...")
        create_directories([self.config.saved_model_dir_path])

    def load_train_data(self):
        x_train = pd.read_csv(Path(self.config.x_train_file_path))
        y_train = pd.read_csv(Path(self.config.y_train_file_path))

        return x_train, y_train

    def train_model(self):
        logger.info(f"Loading training data...")
        x_train, y_train = self.load_train_data()
        logger.info(f"Training data loaded successfully...")

        logger.info(f"Initializing the RandomForestClassifier model...")
        rfc = RandomForestClassifier(
            max_depth = None,
            min_samples_leaf =self.config.param_min_samples_leaf,
            min_samples_split =self.config.param_min_samples_split,
            n_estimators =self.config.param_n_estimators,
        )
        logger.info(f"Fitting the training data in the model...")
        rfc.fit(x_train, y_train)
        logger.info(f"Model Training Complete...")

        logger.info(f"Saving the model at {self.config.saved_model_file_path}...")
        self.save_model(rfc)
        logger.info(f"Model saved at {self.config.saved_model_file_path}...")

        logger.info(f"{'>'*10} Model Training Stage Completed! {'<'*10}")

    def save_model(self, model):
        with open(Path(self.config.saved_model_file_path), "wb") as model_path:
            joblib.dump(model, model_path)
