import pandas as pd
from Customer import utils
from Customer.constants import training
from Customer.exception import CustomerException
from Customer.logger import logging
from Customer.entity.config_entity import DataIngestionConfig
from Customer.entity.artifacts_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split
import os
import sys


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")

            # Exporting collection data as pandas dataframe
            df: pd.DataFrame = utils.get_collection_as_dataframe(database_name=self.data_ingestion_config.database_name,
                                                                 collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Save data in feature store having the shape: {df.shape} ")
            logging.info(f"Columns for the dataframe are : {df.columns} ")

            # Save data in feature store
            logging.info('Create feature store folder if not available')
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            logging.info("Save df to feature store folder")

            # Save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header=True)
            # training and test splitting.
            logging.info('Splitting the data into train and test dataset')
            train_df, test_df = train_test_split(df, test_size=training.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION,
                                                 random_state=1)
            logging.info("create dataset directory folder if not available")

            # create dataset directory folder if not available
            train_path_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(name=train_path_dir, exist_ok=True)
            logging.info('creating the dataset directory folder for test if not available')
            test_path_dir = os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(name=test_path_dir, exist_ok=True)
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info("Preparing the artifact")

            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)
            logging.info(f'Data Ingestion artifact : {data_ingestion_artifact} ')
            return data_ingestion_artifact
        except Exception as e:
            raise CustomerException(e, sys)
