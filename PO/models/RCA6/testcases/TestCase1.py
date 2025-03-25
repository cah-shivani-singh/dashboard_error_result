import sys
sys.path.append('PO\models\RCA6')
from wrapper import general_logger,error_logger
import warnings
warnings.filterwarnings('ignore')
from po_utils.set_process_date import get_json_path
from po_utils.read_sql_queries_from_json import read_description
from po_utils.validation_function import check_ddl_validation



def exec_testcase_1():
    json_path = get_json_path()
    description_of_tc = read_description(rf'{json_path}',1,general_logger,error_logger) 
    general_logger.info(f"TESTCASE 1 - {description_of_tc} \n")
    try:
        res=check_ddl_validation(general_logger,error_logger,rf'{json_path}',r'PO\models\RCA6\rca6_schema.csv',1)
        general_logger.info("-" * 120)
        return res
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 01, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
        general_logger.info("-" * 120)
        return False



