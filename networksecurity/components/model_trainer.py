import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models
)
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import mlflow
import mlflow.sklearn
import dagshub

# Initialize DagsHub MLflow tracking
dagshub.init(repo_owner='abhikdas98', repo_name='networksecurity', mlflow=True)


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Clean MLflow logging
    def log_mlflow(self, best_model, best_model_name, train_metric, test_metric):

        mlflow.log_param("best_model", best_model_name)

        # Train metrics
        mlflow.log_metric("train_f1", train_metric.f1_score)
        mlflow.log_metric("train_precision", train_metric.precision_score)
        mlflow.log_metric("train_recall", train_metric.recall_score)

        # Test metrics
        mlflow.log_metric("test_f1", test_metric.f1_score)
        mlflow.log_metric("test_precision", test_metric.precision_score)
        mlflow.log_metric("test_recall", test_metric.recall_score)

        # Save model in MLflow
        mlflow.sklearn.log_model(best_model, "model")

    def train_model(self, X_train, y_train, X_test, y_test):

        try:
            logging.info("Starting model training")

            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }

            params = {
                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    'learning_rate': [.1, .01, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            # Evaluate models
            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params
            )

            # Get best model
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            logging.info(f"Best model: {best_model_name}")

            # Predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            train_metric = get_classification_score(y_train, y_train_pred)
            test_metric = get_classification_score(y_test, y_test_pred)

            # SINGLE MLflow run (VERY IMPORTANT)
            mlflow.set_experiment("network-security")

            with mlflow.start_run():

                self.log_mlflow(
                    best_model,
                    best_model_name,
                    train_metric,
                    test_metric
                )

            # Load preprocessor
            preprocessor = load_object(
                self.data_transformation_artifact.transformed_object_file_path
            )

            # Fix directory creation
            model_file_path = self.model_trainer_config.trained_model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)

            # Create final model pipeline
            network_model = NetworkModel(
                preprocessor=preprocessor,
                model=best_model
            )

            # Save model correctly
            save_object(
                file_path=model_file_path,
                obj=network_model
            )

            # Optional: Save raw model
            os.makedirs("final_model", exist_ok=True)
            save_object("final_model/model.pkl", best_model)

            # Artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=model_file_path,
                train_metric_artifact=train_metric,
                test_metric_artifact=test_metric
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Load arrays
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            return self.train_model(X_train, y_train, X_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys)