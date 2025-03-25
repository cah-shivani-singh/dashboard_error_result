import sys
sys.path.append('PO\models\RCA11')
from wrapper import general_logger,error_logger
from po_utils.validation_function import validate_data
from po_utils.read_sql_queries_from_json import read_description
from po_utils.set_process_date import get_json_path
from po_utils.count_pass_failed_tescases import increment_count
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os

def exec_testcase_11():
    json_path = get_json_path()
    description_of_tc = read_description(rf'{json_path}',11,general_logger,error_logger) 
    try:
        general_logger.info(f"*******************TESTCASE-11 : {description_of_tc} *******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA6\error_records\TESTCASE11\{timestamp}'
        general_logger.info("Validating : ORDER_CREATE_DTE, Sum_Order_Qty_DC and SAP_SHIP_TO_CUSTOMER_CIN_SHORT_QTY should match the data from source")
        orderdtequery = validate_data(general_logger,error_logger,'PO\models\RCA11\RCA11.json',0,'ORDER_CREATE_DTE',False,11,error_records_folder_name)      
        sumorderdcquery = validate_data(general_logger,error_logger,'PO\models\RCA11\RCA11.json',1,'Sum_Order_Qty_DC',False,11,error_records_folder_name)
        sapcinshortquery = validate_data(general_logger,error_logger,'PO\models\RCA11\RCA11.json',2,'NON-SAP_SHIP_TO_CUSTOMER_CIN_SHORT_QTY',True,11,error_records_folder_name)
        
        general_logger.info("-" * 120)
        if orderdtequery & sumorderdcquery & sapcinshortquery:
            increment_count('pass_tc_count',general_logger,error_logger)
            return True
        else:
            return False    

    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 11, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
        general_logger.info("-" * 120)
        return False


