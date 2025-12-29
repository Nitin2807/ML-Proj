import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass 

@dataclass 
#It tells Python: "This class is just a container for data. Please automatically handle the initialization (__init__), the string representation (__repr__), and comparisons for me."
class DataIngestionConfig:
        train_data_path: str=os.path.join('artifacts','train.csv')
        test_data_path: str=os.path.join('artifacts','test.csv')
        raw_data_path: str=os.path.join('artifacts','data.csv')
#Why I use os.path.join?
#It makes your code Cross-Platform. Windows uses backslashes (\), while Linux/Mac use forward slashes (/). os.path.join ensures your system runs perfectly on your local machine and on a Linux-based Cloud server (AWS/GCP).

class DataIngestion:
        def __init__(self):
                self.ingestion_config=DataIngestionConfig()
                #By calling DataIngestionConfig(), you are triggering that @dataclass you defined earlier. It creates an object that holds three strings: the paths for train, test, and raw data.
        def initiate_data_ingestion(self):
                logging.info("Entered the data ingestion method or component")
                try:
                        df = pd.read_csv('notebook/data/stud.csv')
                        logging.info('Read the dataset as dataframe')

                        os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
                        #exist_ok =Ture means Python checks if the folder exists. If it does, it says "Okay, cool, I'll just keep going." If it doesn't, it creates it.
                        df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
                        logging.info("Train test split initiated")
                        train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
                        train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
                        test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
                        logging.info("Ingestion of the data is completed")
                        return(
                                self.ingestion_config.train_data_path,
                                self.ingestion_config.test_data_path
                        )
                except Exception as e:
                        raise CustomException(e,sys)
                
if __name__=="__main__":
    # Initialize the worker
    obj = DataIngestion()
    
    # Start the ingestion process
    train_data, test_data = obj.initiate_data_ingestion()

    # (Optional) You can pass these to the next step later
    print(f"Ingestion complete. Train path: {train_data}")
