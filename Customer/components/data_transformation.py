import os
import sys
from Customer.entity import config_entity, artifacts_entity
from Customer.exception import CustomerException
from Customer.logger import logging
from typing import Optional
import pandas as pd
import numpy as np


class DataTransformation:
    def __init__(self, data_ingestion_artifact: artifacts_entity.DataIngestionArtifact,
                 data_transformation_config: config_entity.DataTransformationConfig):
        try:
            logging.info(f'{">>" * 20} Data Transformation {"<<" * 20}')
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomerException(error_message=e, error_detail=sys)

    def preprocess_data(self, df):
        try:
            # Dropping null values
            df.dropna(inplace=True)
            # Creating age columns
            df['Age'] = 2015 - df['Year_Birth']
            # Creating age group
            df.loc[df['Age'] <= 19, "AgeGroup"] = "Teen"
            df.loc[(df['Age'] >= 20) & (df['Age'] <= 39), "AgeGroup"] = "Adults"
            df.loc[(df['Age'] >= 40) & (df['Age'] <= 59), "AgeGroup"] = "Middle Age Adults"
            df.loc[(df['Age'] >= 60), "AgeGroup"] = "Seniors"
            # Creating some extra columns by aggregating them
            df['TotalSpendings'] = df['MntFruits'] + df['MntWines'] + df['MntMeatProducts'] + df['MntFishProducts'] + \
                                   df['MntSweetProducts'] + df['MntGoldProds']
            df['Children'] = df['Kidhome'] + df['Teenhome']
            df.Marital_Status = df.Marital_Status.replace({
                "Together": "Married",
                "Divorced": "Single",
                "Widow": "Single",
                "Alone": "Single",
                "Absurd": "Single",
                "YOLO": "Single"
            })
            # Converting to datetime
            df.Dt_Customer = pd.to_datetime(df.Dt_Customer)

            # Month Enrollment
            df['MonthEnrollment'] = (2015 - df.Dt_Customer.dt.year) * 12 + (1 - df.Dt_Customer.dt.month)
            # Dropping outliers from Age & Income
            df = df[df['Age'] < 100]
            df = df[df['Income'] < 110000]

            # Drop unnecessary columns
            df = df.drop(
                [
                    'ID', 'Year_Birth', 'Education', 'Marital_Status', 'Kidhome',
                    'Teenhome', 'Dt_Customer', 'MntWines', 'MntFruits', 'MntMeatProducts',
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
                    'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth',
                    'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1',
                    'AcceptedCmp2', 'Complain', 'Z_CostContact', 'Z_Revenue', 'Response', 'AgeGroup'
                ],

                axis=1
            )

            return df
        except Exception as e:
            raise CustomerException(error_message=e, error_detail=sys)

    def initiate_data_transformation(self) -> artifacts_entity.DataTransformationArtifact:
        try:
            logging.info(f"{'=' * 20}Data Transformation log started.{'=' * 20} ")

            # Load train data
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path, sep=';')
            logging.info(f" Shape of the train data file: {train_df.shape}")
            train_df = self.preprocess_data(train_df)
            logging.info(f" Shape of transformed data file: {train_df.shape}")
            logging.info("Data Transformation is completed")

            # Save the cleaned train data for transformation
            transformed_path_dir = os.path.dirname(self.data_transformation_config.transformed_train_path)
            os.makedirs(name=transformed_path_dir, exist_ok=True)
            train_df.to_csv(path_or_buf=self.data_transformation_config.transformed_train_path, index=False,
                            header=True)
            logging.info("Preparing the artifact for transformation")
            data_transform_artifact = artifacts_entity.DataTransformationArtifact(
                transformed_train_path=self.data_transformation_config.transformed_train_path
            )
            logging.info(f"Saved transformed data to {self.data_transformation_config.transformed_train_path}")
            return data_transform_artifact
        except Exception as e:
            raise CustomerException(e, sys)
