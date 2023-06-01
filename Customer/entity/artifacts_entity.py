from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_train_path: str


@dataclass
class ModelTrainerArtifact:
    model_path: str
