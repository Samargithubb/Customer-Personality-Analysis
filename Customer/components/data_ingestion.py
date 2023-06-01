import pandas as pd
from Customer import utils
from Customer.exception import CustomerException
from Customer.logger import logging
from Customer.entity.config_entity import DataIngestionConfig
from Customer.entity.artifacts_entity import DataIngestionArtifact
import os
import sys


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"{'=' * 20}Data Insertion log started.{'=' * 20} ")
            logging.info(f"Exporting collection data as pandas dataframe")

            # Exporting collection data as pandas dataframe
            df: pd.DataFrame = utils.get_collection_as_dataframe(database_name=self.data_ingestion_config.database_name,
                                                                 collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Save data in feature store having the shape: {df.shape} ")
            logging.info(f"Columns for the dataframe are : {df.columns} ")

            logging.info("create dataset directory folder if not available")
            # create dataset directory folder if not available
            train_path_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(name=train_path_dir, exist_ok=True)
            df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, index=False, header=True, sep=',')
            logging.info("Data Ingestion Completed")
            logging.info("Preparing the artifact")
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path)
            logging.info(f'Data Ingestion artifact : {data_ingestion_artifact} ')
            return data_ingestion_artifact
        except Exception as e:
            raise CustomerException(e, sys)
