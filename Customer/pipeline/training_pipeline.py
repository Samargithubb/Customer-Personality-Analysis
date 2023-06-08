import sys
from Customer.logger import logging
from Customer.exception import CustomerException
from Customer.entity import config_entity
from Customer.components.data_ingestion import DataIngestion
from Customer.components.data_transformation import DataTransformation
from Customer.components.model_trainer import ModelTrainer


def start_training_pipeline():
    try:
        logging.info("***********************TRAINING START***************************")
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # Data Transformation
        data_transformation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_transformation = DataTransformation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_transformation_config=data_transformation_config
        )
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        # Model Training
        model_trainer_config = config_entity.ModelTrainerConfig(
            training_pipeline_config=training_pipeline_config
        )
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact
        )
        model_trainer.initiate_model_training()

        logging.info("***********************TRAINING COMPLETED ******************************")
    except Exception as e:
        raise CustomerException(e, sys)

