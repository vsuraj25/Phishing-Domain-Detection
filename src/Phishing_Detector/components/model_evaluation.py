from pathlib import Path
from Phishing_Detector.utils import *
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from Phishing_Detector.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:
    
    def __init__(self, config:ModelEvaluationConfig):
        logger.info(f"{'>'*10} Starting Model Evaluation Stage! {'<'*10}")
        
        logger.info(f"Getting Configuration for Model Evaluation Stage...")
        self.config = config
        logger.info(f"Configurations : {config}")

        logger.info(f"Creating required directories...")
        create_directories([self.config.model_metrics_dir_path])


    def evaluate_metrics(self):
        logger.info(f"Loading training data...")
        x_test, y_test  = self._load_test_data()
        logger.info(f"Testing data loaded successfully...")

        logger.info(f"Loading model for evaluation...")
        model = self._load_model()
        logger.info(f"Model loaded successfully...")

        logger.info(f"Prediction on test data...")
        y_prob = model.predict(x_test)

        self._eval_and_save_metrics(actual = y_test,
                                    predicted = y_prob,
                                    save_metrics_path = Path(self.config.model_metrics_json_file_path),
                                    save_cmat_path = Path(self.config.model_metrics_cmat_file_path))

    def _load_test_data(self):
        x_test = pd.read_csv(Path(self.config.x_test_file_path))
        y_test = pd.read_csv(Path(self.config.y_test_file_path))

        return x_test, y_test

    def _load_model(self):
        with open(Path(self.config.saved_model_file_path), 'rb') as model_file:
            model = joblib.load(model_file)
        return model
    
    def _eval_and_save_metrics(self,actual, predicted, save_metrics_path, save_cmat_path):
        logger.info(f"Starting metrics evaluation...")
        acc_score = round(accuracy_score(actual, predicted), 4)
        rec_score = round(recall_score(actual, predicted),4)
        prec_score = round(precision_score(actual, predicted),4)
        f1 = round(f1_score(actual, predicted))
        confusion_mat = confusion_matrix(actual, predicted)
        cm_display = ConfusionMatrixDisplay(confusion_matrix = confusion_mat, display_labels = [False, True])

        report = {
            "Accuracy Score" : acc_score,
            "Recall Score" : rec_score,
            "Precision Score" : prec_score,
            "F1 Score" : f1,
        }
        logger.info(f"Evaluation Result : \n {report}")
        logger.info(f"Confusion Matrix : \n {confusion_mat}")

        logger.info(f"Saving Evaluation Report at {save_metrics_path}")
        save_json(path = Path(save_metrics_path), data = report)
        logger.info(f"Evaluation Report saved at {save_metrics_path}")

        logger.info(f"Saving Confusion Matrix Report at {save_cmat_path}")
        cm_display.plot()
        plt.savefig(Path(save_cmat_path))
        logger.info(f"Confusion Matrix Report saved at {save_cmat_path}")