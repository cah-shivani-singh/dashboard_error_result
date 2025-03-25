import sys
sys.path.append('PO\models\RCA6')
from wrapper import general_logger,error_logger
import warnings
warnings.filterwarnings('ignore')
from po_utils.set_process_date import get_json_path
from po_utils.read_sql_queries_from_json import read_description
from po_utils.validation_function import check_duplicate
from datetime import datetime

def exec_testcase_2():
    try:
        json_path = get_json_path()
        description_of_tc = read_description(rf'{json_path}',2,general_logger,error_logger)
        general_logger.info(f"TESTCASE 2 - {description_of_tc} \n ")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA6\error_records\TESTCASE2\{timestamp}'
        res=check_duplicate(general_logger,error_logger,2,rf'{json_path}',error_records_folder_name)
        general_logger.info("-" * 120)
        return res
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 02, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
        general_logger.info("-" * 120)
        return False
