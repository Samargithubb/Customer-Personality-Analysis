import os
import sys
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
from Customer.constants import training
from Customer.entity import config_entity, artifacts_entity
from Customer.logger import logging
from Customer.exception import CustomerException
from Customer import utils


class ModelTrainer:
    def __init__(self, data_transformation_artifact: artifacts_entity.DataTransformationArtifact,
                 model_trainer_config: config_entity.ModelTrainerConfig):
        try:
            logging.info(f"{'>>' * 20} Model Trainer {'<<' * 20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomerException(e, sys)

    def train_model(self):
        try:
            logging.info("Loading data from transformed dir for training the model")
            df = pd.read_csv(self.data_transformation_artifact.transformed_train_path)

            inertiaRange = []
            silhouette = []

            for i in training.CLUSTER_RANGE:
                model_m = KMeans(n_clusters=i)
                model_m.fit(df)
                inertiaRange.append(model_m.inertia_)
                silhouette.append(metrics.silhouette_score(df, model_m.labels_))

            os.makedirs(self.model_trainer_config.model_path, exist_ok=True)
            plt.plot(training.CLUSTER_RANGE, inertiaRange)
            image_elbow = os.path.join(self.model_trainer_config.model_path, "elbow_plot.png")

            plt.savefig(image_elbow)
            logging.info("Saved elbow img")

            # Find the index of the knee point on the inertia plot
            knee_index = next(k for k in range(1, len(inertiaRange) - 1) if
                              inertiaRange[k - 1] - inertiaRange[k] > inertiaRange[k] - inertiaRange[k + 1]) + 1

            # Use the knee point index to determine the optimal number of clusters
            optimal_clusters = knee_index + 1

            logging.info(f"Optimal Number of cluster based on knee plot is {optimal_clusters}")
            # Fit the KMeans model with the optimal number of clusters
            model = KMeans(n_clusters=optimal_clusters)
            model.fit(df)

            # Saving model
            file_name = os.path.join(self.model_trainer_config.model_path, 'model.pkl')
            pickle.dump(model, open(file_name, 'wb'))
            logging.info("Model Saved Successfully")
        except Exception as e:
            raise CustomerException(e, sys)

    def initiate_model_training(self):
        try:
            logging.info(f"{'=' * 20} Model Training log started.{'=' * 20} ")
            self.train_model()
            logging.info(f"{'=' * 20}Model Trainer  completed.{'=' * 20} \n\n")

            modelTrainerArtifact = artifacts_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path
            )
            return modelTrainerArtifact

        except Exception as e:
            raise CustomerException(e, sys)


