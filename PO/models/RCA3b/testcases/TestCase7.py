##########################################Scenario: Sales orders in rca 3b table should not be rejected due to reasons other than a DC inventory issue When searched for a particular sales order Then the rejection condition should be 'Z6' or null Then either lf_shrt_id<>'S' and lf_short_code<>'01' #####################

import sys
sys.path.append('PO\models\RCA3b')
from wrapper import general_logger,error_logger
from po_utils import validate_data
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')
def exec_testcase_7():
    try:
        general_logger.info("*******************TESTCASE-07 : Sales orders in rca 3b table should not be rejected due to reasons other than a DC inventory issue When searched for a particular sales order Then the rejection condition should be 'Z6' or null Then either lf_shrt_id<>'S' and lf_short_code<>'01' ***********************")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_records_folder_name=rf'PO\models\RCA3b\error_records\TESTCASE7\{timestamp}'
        validate_data(general_logger,error_logger,'PO\models\RCA3b\RCA3b.json',0,None,True,7,error_records_folder_name)
    except Exception as e:
        general_logger.info("Error executing Validation for TestCase - 07, check error log file for more details")
        error_logger.error(f"Unexpected error occured : {e}")
    general_logger.info("-" * 120)



