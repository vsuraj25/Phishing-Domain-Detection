from Phishing_Detector.entity.config_entity import DataValidationConfig
from Phishing_Detector.utils import *
from Phishing_Detector.constants import *
from Phishing_Detector import logger, DataNotValid
import pandas as pd

class DataValidation:
    
    def __init__(self, config:DataValidationConfig):
        self.config = config
        create_directories([self.config.validation_report_dir_path])
        
    def validate_data(self):

        def validate_columns(schema, df):
            logger.info("Validating columns.")
            cols_validation_status = False
            cols_dtype_validation_status = False
            for i in df.columns:
                if i not in list(schema.keys()):
                    cols_validation_status = False
                    logger.info(f"Invalid columns found - {i}.")
                    break
                else:
                    cols_validation_status = True
                
                if df[i].dtype != schema[i]:
                    cols_dtype_validation_status = False
                    logger.info(f"Invalid data type found - {i} : {df[i].dtype}.")
                    break
                else:
                    cols_dtype_validation_status = True

            if cols_validation_status and cols_dtype_validation_status:
                logger.info("All Columns are valid.")
            else:
                logger.info("Failed to validate columns.")

            return cols_validation_status, cols_dtype_validation_status

        def validate_no_of_cols(schema_no_of_cols, df):
            logger.info("Validating number of columns...")
            validation_status = False

            if schema_no_of_cols == df.shape[1]:
                validation_status = True
                logger.info("Valid number of columns found.")
            else:
                validation_status = False
                logger.info(f"Invalid no of columns - {df.shape[1]}.")
                logger.info("Failed to validate total number of columns.")
                
            return validation_status

        def validate_no_of_rows(schema_no_of_rows, df):
            logger.info("Validating number of rows.")
            validation_status = False
            
            if schema_no_of_rows == df.shape[0]:
                validation_status = True
                logger.info("Valid number of rows found.")
            else:
                validation_status = False
                logger.info(f"Invalid no of rows - {df.shape[0]}.")
                logger.info("Failed to validate total number of rows.")
            
            return validation_status

        try:
            logger.info(f"{'>'*10} Starting Data Validation Stage! {'<'*10}")
            logger.info("Reding validation schema...")
            schema = self.config.schema
            schema_columns = schema['columns']
            schema_total_cols = schema['no_of_cols']
            schema_total_rows = schema['no_of_rows']
            logger.info("Loading the data...")
            df = pd.read_csv(Path(self.config.processed_data_file_path))
            
            val_cols, val_dtypes = validate_columns(schema_columns, df)
            val_total_cols = validate_no_of_cols(schema_total_cols,df)
            val_total_rows = validate_no_of_rows(schema_total_rows, df)
            validation_status = val_cols and val_dtypes and val_total_cols and val_total_rows

            logger.info(f"Saving Validation report at {self.config.validation_report_file_path}...")
            report = {'is_cols_valid' : val_cols,
                      'is_dtypes_valid' : val_dtypes,
                      'is_total_cols_valid' : val_total_cols,
                      'is_total_rows_valid' : val_total_rows,
                      'final_validation_status' : validation_status,
                      }
            
            save_json(path = Path(self.config.validation_report_file_path), data = report)
            logger.info(f"Validation report saved at {self.config.validation_report_file_path}.")

            if validation_status:
                logger.info(f"{'>'*10} Data Validation Stage Completed Successfully! {'<'*10}")
            else:
                logger.error(e)
                raise DataNotValid
        except Exception as e:
            raise e


        
