# Data Base realated constant variable
DATABASE_NAME = "CPA_DB"
COLLECTION_NAME = "customer"

# defining common constant variable for training pipeline
PIPELINE_NAME: str = "Customer"
ARTIFACT_DIR: str = "artifact"
DATA_FILE_PATH = 'customer_data.csv'
TRAIN_FILE_NAME: str = "train.csv"
FILE_NAME = "customer.csv"


"""

Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "Customer"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"


"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"

"""
Model Trainer related constant start with MODE TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model"
CLUSTER_RANGE = range(2, 21)
