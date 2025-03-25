import sys
sys.path.append('PO\models\RCA11')
from wrapper import general_logger,error_logger
import warnings
warnings.filterwarnings('ignore')
from po_utils.set_process_date import get_json_path
from po_utils.read_sql_queries_from_json import read_description
from po_utils.validation_function import validate_data
from po_utils.count_pass_failed_tescases import increment_count
from datetime import datetime

warnings.filterwarnings('ignore')
def exec_testcase_4():
    try:
        json_path = get_json_path()
        description_of_tc = read_description(rf'{json_path}',4,general_logger,error_logger) 
        general_logger.info(f"TESTCASE 4 - {description_of_tc} \n")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA11\error_records\TESTCASE4\{timestamp}'
        general_logger.info("Validationg : Order Delivery status is correctly calculated as 'Late'")
        nul_res = validate_data(general_logger,error_logger,'PO\models\RCA11\RCA11.json',0,None,False,4,error_records_folder_name)
        general_logger.info("Validationg : all records should display Order Delivery Status as 'Late'")
        shortcode_res = validate_data(general_logger,error_logger,'PO\models\RCA11\RCA11.json',1,None,True,4,error_records_folder_name)
        if nul_res & shortcode_res:
            increment_count('pass_tc_count',general_logger,error_logger)

    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 4, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)

