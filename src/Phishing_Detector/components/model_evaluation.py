from pathlib import Path
from Phishing_Detector.utils import *
from Phishing_Detector.sec import *
from urllib.parse import urlparse
import pandas as pd
import mlflow
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt
from Phishing_Detector.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        logger.info(f"{'>'*10} Starting Model Evaluation Stage! {'<'*10}")

        logger.info(f"Getting Configuration for Model Evaluation Stage...")
        self.config = config
        logger.info(f"Configurations : {config}")

        os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
        os.environ["MLFLOW_TRACKING_USERNAME"] = MLFLOW_TRACKING_USERNAME
        os.environ["MLFLOW_TRACKING_PASSWORD"] = MLFLOW_TRACKING_PASSWORD

        logger.info(f"Creating required directories...")
        create_directories([self.config.model_metrics_dir_path])

    def eval_metrics_and_log_into_mlflow(self):
        logger.info(f"Loading training data...")
        x_test, y_test = self._load_test_data()
        logger.info(f"Testing data loaded successfully...")

        logger.info(f"Loading model for evaluation...")
        model = self._load_model()
        logger.info(f"Model loaded successfully...")

        logger.info(f"Prediction on test data...")
        y_prob = model.predict(x_test)

        metrics = self._eval_and_save_metrics(
            actual=y_test,
            predicted=y_prob,
            save_metrics_path=Path(self.config.model_metrics_json_file_path),
            save_cmat_path=Path(self.config.model_metrics_cmat_file_path),
        )

        logger.info(f"MLFlow tracking started...")
        mlflow.set_registry_uri(MLFLOW_TRACKING_URI)
        tracking_uri_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run():
            logger.info(f"Logging all parameters in mlflow...")
            mlflow.log_param("max_depth", self.config.param_max_depth)
            mlflow.log_param("min_samples_leaf", self.config.param_min_samples_leaf)
            mlflow.log_param("min_samples_split", self.config.param_min_samples_split)
            mlflow.log_param("n_estimators", self.config.param_n_estimators)
            logger.info(f"Logging all metrics in mlflow...")
            mlflow.log_metrics(
                {
                    "accuracy_score": metrics[0],
                    "recall_score": metrics[1],
                    "precision_score": metrics[2],
                    "f1_score": metrics[3],
                }
            )
            if tracking_uri_type_store != "file":
                mlflow.sklearn.log_model(
                    model,
                    "model",
                    registered_model_name=self.config.param_reg_model_name,
                )
            else:
                mlflow.sklearn.log_model(model, "model")

            logger.info(
                f"MLFlow tracking complete, you can visualize your model results using the command `mlflow ui` or globally at https://dagshub.com/vsuraj25/DeepCNN_Classifier_End_To_End.mlflow"
            )

    def _load_test_data(self):
        x_test = pd.read_csv(Path(self.config.x_test_file_path))
        y_test = pd.read_csv(Path(self.config.y_test_file_path))

        return x_test, y_test

    def _load_model(self):
        with open(Path(self.config.saved_model_file_path), "rb") as model_file:
            model = joblib.load(model_file)
        return model

    def _eval_and_save_metrics(
        self, actual, predicted, save_metrics_path, save_cmat_path
    ):
        logger.info(f"Starting metrics evaluation...")
        acc_score = round(accuracy_score(actual, predicted), 4)
        rec_score = round(recall_score(actual, predicted), 4)
        prec_score = round(precision_score(actual, predicted), 4)
        f1 = round(f1_score(actual, predicted))
        confusion_mat = confusion_matrix(actual, predicted)
        cm_display = ConfusionMatrixDisplay(
            confusion_matrix=confusion_mat, display_labels=[False, True]
        )

        report = {
            "Accuracy Score": acc_score,
            "Recall Score": rec_score,
            "Precision Score": prec_score,
            "F1 Score": f1,
        }
        logger.info(f"Evaluation Result : \n {report}")
        logger.info(f"Confusion Matrix : \n {confusion_mat}")

        logger.info(f"Saving Evaluation Report at {save_metrics_path}")
        save_json(path=Path(save_metrics_path), data=report)
        logger.info(f"Evaluation Report saved at {save_metrics_path}")

        logger.info(f"Saving Confusion Matrix Report at {save_cmat_path}")
        cm_display.plot()
        plt.savefig(Path(save_cmat_path))
        logger.info(f"Confusion Matrix Report saved at {save_cmat_path}")
        return [acc_score, rec_score, prec_score, f1]
