from Phishing_Detector.components import ModelEvaluation
from Phishing_Detector.config import ConfigurationManager


def main():
    config = ConfigurationManager()
    model_evaluation_config = config.get_model_evaluation_config()
    model_evaluation = ModelEvaluation(config=model_evaluation_config)
    model_evaluation.eval_metrics_and_log_into_mlflow()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
