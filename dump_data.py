import pandas as pd
import json
from Customer.configuration import mongo_client
from Customer.constants import training


if __name__ == "__main__":
    df = pd.read_csv(training.DATA_FILE_PATH)
    print(f'Rows and Columns: {df.shape}')

    # convert dataframe to json format so that we can dump the records into mongodb
    df.reset_index(drop=True, inplace=True)

    json_records = list(json.loads(df.T.to_json()).values())
    print(json_records[0])

    # inserted converted json record to mongodb
    mongo_client[training.DATABASE_NAME][training.COLLECTION_NAME].insert_many(json_records)
