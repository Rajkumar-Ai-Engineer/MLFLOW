import sys 

from sklearn.linear_model import ElasticNet

from sklearn.metrics import (
    mean_absolute_error,mean_squared_error,root_mean_squared_error,r2_score
)

from sklearn.model_selection import train_test_split

import pandas as pd 

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import logging 

from urllib.parse import urlparse


logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

def eval_metrics(actual,pred):
    rmse = root_mean_squared_error(actual,pred)
    mae = mean_absolute_error(actual,pred)
    mse = mean_squared_error(actual,pred)
    r2 = r2_score(actual,pred)
    return rmse,mae,mse,r2 

if __name__ == "__main__":
    try:
        logger.info("starting")
        data_uri = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-white.csv"
        data = pd.read_csv(data_uri,sep=";")
        
        train,test = train_test_split(data,test_size=0.2)
        
        train_x = train.drop(["quality"],axis=1)
        train_y = train[["quality"]]
        test_x = test.drop(["quality"],axis=1)
        test_y = test[["quality"]]
        
        alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
        l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
        
        with mlflow.start_run():
            lr = ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=42)
            lr.fit(train_x,train_y)
            
            predicted_data = lr.predict(test_x)
            (rmse,mae,mse,r2) = eval_metrics(test_y,predicted_data)
            
            print("Elastic Net model (alpha={:f}) and (l1_ratio={:f}):".format(alpha,l1_ratio))
            print("rmse:",rmse)
            print("mse:",mse)
            print("mae:",mae)
            print("r2:",r2)
            
            mlflow.log_param("alpha",alpha)        
            mlflow.log_param("l1_ratio",l1_ratio)
            mlflow.log_metric("rmse",rmse)
            mlflow.log_metric("mse",mse)
            mlflow.log_metric("mae",mae)
            mlflow.log_metric("r2",r2)
            
            predictions = lr.predict(train_x)
            signature = infer_signature(train_x,predictions)
            
            tracking_uri_scheme = urlparse(mlflow.get_tracking_uri()).scheme
            
            if tracking_uri_scheme !="file":
                mlflow.sklearn.log_model(
                    lr,"model",registered_model_name="ElasticNetWineModel",signature=signature
                )
                
            else:
                mlflow.sklearn.log_model(
                    lr,"model",signature=signature
                )
                
                
    except Exception as e:
        raise e



