import glob
import os
import sys
import pickle
from Customer.exception import CustomerException
from datetime import datetime


class ModelResolver:
    def __init__(self):
        try:
            # Get the latest timestamp folder
            timestamp_folders = glob.glob('artifact/*/')
            latest_timestamp_folder = max(timestamp_folders, key=lambda x: datetime.strptime(os.path.basename(x[:-1]),
                                                                                             "%m_%d_%Y_%H_%M_%S"))

            # Get the latest model path
            model_folder = os.path.join(latest_timestamp_folder, 'model_trainer', 'model')
            model_path = os.path.join(model_folder, 'model.pkl')

            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)

        except Exception as e:
            raise CustomerException(e, sys)

    def get_model(self):
        return self.model

    def predict(self, data):
        return self.model.predict(data)
