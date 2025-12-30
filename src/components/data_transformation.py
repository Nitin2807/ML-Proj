import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import os
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl') 

class datatransforation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = ['gender',
                                    'race_ethnicity',
                                    'parental_level_of_education',
                                    'lunch',
                                    'test_preparation_course']  
            num_pipeline = Pipeline(
                steps =[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]) 
            categorical_pipeline = Pipeline(
                steps =[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            ) 
            logging.info(f'Numerical columns: {numerical_columns} transformation done')
            logging.info(f'Categorical columns: {categorical_columns} transformation done')
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipeline', categorical_pipeline, categorical_columns)
                ])
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('Read train and test data completed')
            logging.info('Obtaining preprocessor object')
            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            #it is separated from the training data sos that the transformation is not applied on the target column
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)  
            target_feature_test_df = test_df[target_column_name]
            logging.info('Applying preprocessing object on training and testing dataframes')
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            #we use fit_transform on training data because we want to fit the preprocessor on training data and then transform it
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            #we don't use fit_transform on test data because we don't wanna learn from the test data. We only want to transform it based on what we learned from the training data.
            #if one applies fit_transform on test data, it will lead to data leakage(i.e., good performance on test data but poor performance on real world data)
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            #The np.c_ (short for column-wise concatenation) is a special object in NumPy that allows you to stack arrays horizontally (side-by-side)
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            logging.info('saved preprocessing object')
            save_object(file_path= self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)