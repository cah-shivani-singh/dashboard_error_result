######################################### To verify whether the supplier type is correctly tagged,When searched for any process date for any CIN and DC,Then CF_Supplier_Type should be correctly tagged as 'CENTRALIZED','NONCENTRALIZED' or 'HUBSPOKE'  ###############################
import sys
sys.path.append('PO\models\RCA1')
from wrapper import general_logger,error_logger
from po_utils.validation_function import validate_data
from po_utils.read_sql_queries_from_json import read_description
from po_utils.set_process_date import get_json_path
from po_utils.count_pass_failed_tescases import increment_count
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os

def exec_testcase_4():
    json_path = get_json_path()
    description_of_tc = read_description(rf'{json_path}',4,general_logger,error_logger)
    try:
        general_logger.info(f"*******************TESTCASE-04 : {description_of_tc} *******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA1\error_records\TESTCASE4\{timestamp}'

        centr_res = validate_data(general_logger,error_logger,'PO\models\RCA1\RCA1.json',0,'CENTRALIZED',False,4,error_records_folder_name)
        hubspk_res = validate_data(general_logger,error_logger,'PO\models\RCA1\RCA1.json',1,'HUBSPOKE',False,4,error_records_folder_name)
        non_centr = validate_data(general_logger,error_logger,'PO\models\RCA1\RCA1.json',2,'NON-CENTRALIZED',True,4,error_records_folder_name)
        general_logger.info("-" * 120)
        if centr_res & hubspk_res & non_centr:
            increment_count('pass_tc_count',general_logger,error_logger)
            return True
        else:
            return False    

    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 04, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
        general_logger.info("-" * 120)
        return False

exec_testcase_4()
