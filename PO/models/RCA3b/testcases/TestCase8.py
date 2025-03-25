##########################################Scenario: All invoices in the table should have short code as not null When searched for a shorted invoice Then the value of LF_Short_Code should match with the source And LF_Short_Code should not be null #####################
import sys
sys.path.append('PO\models\RCA3b')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

def exec_testcase_8():
    try:
        general_logger.info("*******************TESTCAS-8 :  All invoices in the table should have short code as not null When searched for a shorted invoice Then the value of LF_Short_Code should match with the source And LF_Short_Code should not be null*******************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3b\error_records\TESTCASE8\{timestamp}'
        general_logger.info("Validating the value of LF_Short_Code should match with the source")
        validate_data(general_logger,error_logger,'PO\models\RCA3b\RCA3b.json',0,'lf_Short_code_value',False,8,error_records_folder_name)
        general_logger.info("Validating the value of LF_Short_Code should not be null")
        validate_data(general_logger,error_logger,'PO\models\RCA3b\RCA3b.json',1,'lf_Short_code_is_null',True,8,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 8, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)

