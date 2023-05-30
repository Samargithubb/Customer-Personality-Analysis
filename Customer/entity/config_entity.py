from datetime import datetime
import os, sys
from Customer.constants import training
from Customer.exception import CustomerException


class TrainingPipelineConfig:

    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = training.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(training.ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.database_name = training.DATABASE_NAME
        self.collection_name = training.COLLECTION_NAME
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir, training.DATA_INGESTION_INGESTED_DIR
        )
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir, training.DATA_INGESTION_FEATURE_DIR, training.FILE_NAME
        )
        self.train_file_path = os.path.join(
            self.data_ingestion_dir, "Dataset", training.TRAIN_FILE_NAME
        )
        self.test_file_path = os.path.join(
            self.data_ingestion_dir, "Dataset", training.TEST_FILE_NAME
        )

        def to_dict(self,):
            try:
                return self.__dict__

            except Exception as e:
                raise CustomerException(e, sys)
